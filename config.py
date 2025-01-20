RANKING_URLS = {
    'daily': 'https://www.pixiv.net/ranking.php?mode=daily&content=illust',
    'weekly': 'https://www.pixiv.net/ranking.php?mode=weekly&content=illust',
    'monthly': 'https://www.pixiv.net/ranking.php?mode=monthly&content=illust',
    'rookie': 'https://www.pixiv.net/ranking.php?mode=rookie&content=illust'
}

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
    'Referer': 'https://www.pixiv.net/'
}

IPFS_UPLOAD_URL = 'https://ipfs-relay.crossbell.io/upload'

# 并发设置
MAX_CONCURRENT_DOWNLOADS = 3
MAX_RETRIES = 3
RETRY_DELAY = 5  # 秒

# 输出文件
OUTPUT_FILES = {
    'daily': 'daily.json',
    'weekly': 'weekly.json',
    'monthly': 'monthly.json',
    'rookie': 'rookie.json'
} 