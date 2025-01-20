import asyncio
import json
import logging
from pathlib import Path
from typing import List, Dict, Any
import httpx
from bs4 import BeautifulSoup
import aiofiles
from config import RANKING_URLS, HEADERS, IPFS_UPLOAD_URL, OUTPUT_FILES, MAX_CONCURRENT_DOWNLOADS, MAX_RETRIES, RETRY_DELAY

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class PixivCrawler:
    def __init__(self):
        self.client = httpx.AsyncClient(headers=HEADERS, timeout=30.0)
        self.semaphore = asyncio.Semaphore(MAX_CONCURRENT_DOWNLOADS)

    async def close(self):
        await self.client.aclose()

    async def fetch_page(self, url: str) -> str:
        """获取页面内容"""
        for _ in range(MAX_RETRIES):
            try:
                response = await self.client.get(url)
                response.raise_for_status()
                return response.text
            except httpx.HTTPError as e:
                logger.error(f"Error fetching {url}: {e}")
                await asyncio.sleep(RETRY_DELAY)
        raise Exception(f"Failed to fetch {url} after {MAX_RETRIES} retries")

    def parse_image_data(self, html: str) -> List[Dict[str, Any]]:
        """解析HTML中的图片数据"""
        soup = BeautifulSoup(html, 'html.parser')
        images = []
        for img in soup.select('img._thumbnail'):
            if not img.get('data-id'):
                continue
            
            data_src = img.get('data-src', '')
            # 移除缩略图参数
            data_src = data_src.replace('/c/240x480', '')
            
            image_data = {
                'data-id': img.get('data-id'),
                'data-tags': img.get('data-tags', ''),
                'data-src': [data_src],  # 使用列表存储，方便多P情况
                'web2url': []  # 预留IPFS URL
            }
            images.append(image_data)
        return images

    async def check_multi_pages(self, base_url: str) -> List[str]:
        """检查是否为多P作品"""
        urls = [base_url]
        base, ext = base_url.rsplit('_p0_', 1)
        page = 1
        
        while True:
            next_url = f"{base}_p{page}_{ext}"
            try:
                response = await self.client.head(next_url)
                if response.status_code == 404:
                    break
                urls.append(next_url)
                page += 1
            except httpx.HTTPError:
                break
        
        return urls

    async def download_and_upload_to_ipfs(self, url: str) -> str:
        """下载图片并上传到IPFS"""
        async with self.semaphore:
            try:
                # 下载图片
                response = await self.client.get(url)
                response.raise_for_status()
                image_data = response.content

                # 上传到IPFS
                files = {'file': ('image.jpg', image_data)}
                response = await self.client.post(IPFS_UPLOAD_URL, files=files)
                response.raise_for_status()
                result = response.json()
                
                return result['web2url']
            except Exception as e:
                logger.error(f"Error processing {url}: {e}")
                return ""

    async def process_ranking(self, mode: str):
        """处理特定排行榜"""
        url = RANKING_URLS[mode]
        output_file = OUTPUT_FILES[mode]
        
        # 确保输出文件存在
        if not Path(output_file).exists():
            await self.save_json(output_file, [])

        # 读取现有数据
        existing_data = await self.load_json(output_file)
        existing_ids = {item['data-id'] for item in existing_data}

        # 获取新数据
        html = await self.fetch_page(url)
        new_images = self.parse_image_data(html)

        # 处理新数据
        for image in new_images:
            if image['data-id'] in existing_ids:
                continue

            # 检查多P
            base_url = image['data-src'][0]
            all_urls = await self.check_multi_pages(base_url)
            image['data-src'] = all_urls

            # 下载并上传到IPFS
            web2urls = []
            for url in all_urls:
                ipfs_url = await self.download_and_upload_to_ipfs(url)
                if ipfs_url:
                    web2urls.append(ipfs_url)
            image['web2url'] = web2urls

            # 添加到现有数据
            existing_data.append(image)

        # 排序和去重
        existing_data.sort(key=lambda x: int(x['data-id']), reverse=True)
        await self.save_json(output_file, existing_data)

    async def load_json(self, filename: str) -> List[Dict]:
        """加载JSON文件"""
        try:
            async with aiofiles.open(filename, 'r', encoding='utf-8') as f:
                content = await f.read()
                return json.loads(content) if content else []
        except FileNotFoundError:
            return []

    async def save_json(self, filename: str, data: List[Dict]):
        """保存JSON文件"""
        async with aiofiles.open(filename, 'w', encoding='utf-8') as f:
            await f.write(json.dumps(data, ensure_ascii=False, indent=2))

async def main():
    crawler = PixivCrawler()
    try:
        # 并发处理所有排行榜
        tasks = [crawler.process_ranking(mode) for mode in RANKING_URLS.keys()]
        await asyncio.gather(*tasks)
    finally:
        await crawler.close()

if __name__ == "__main__":
    asyncio.run(main()) 