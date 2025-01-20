import json
from pathlib import Path

def load_json(file_path):
    """加载JSON文件"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def generate_html():
    """生成HTML页面"""
    # 加载所有JSON数据
    data = {
        'daily': load_json('daily.json'),
        'weekly': load_json('weekly.json'),
        'monthly': load_json('monthly.json'),
        'rookie': load_json('rookie.json')
    }
    
    # HTML模板
    html = '''
<!DOCTYPE html>
<html lang="zh">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Pixiv IPFS Gallery</title>
    <link rel="icon" type="image/png" href="https://q2.qlogo.cn/headimg_dl?dst_uin=2973517380&spec=5">
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: #f5f5f5;
            margin: 0;
            min-height: 100vh;
        }
        
        .container {
            max-width: 100%;
            margin: 0 auto;
            padding: 20px;
        }
        
        .tabs {
            display: flex;
            gap: 10px;
            margin-bottom: 20px;
            position: sticky;
            top: 0;
            background: #f5f5f5;
            padding: 10px 20px;
            z-index: 100;
        }
        
        .tab {
            padding: 10px 20px;
            background: #fff;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            font-size: 16px;
            transition: all 0.3s ease;
        }
        
        .tab.active {
            background: #0066cc;
            color: white;
        }
        
        .gallery {
            width: 100%;
            margin: 0 auto;
            padding: 0 20px;
        }
        
        .gallery > div {
            display: none;
        }
        
        .gallery > div.active {
            display: grid;
            grid-template-columns: repeat(1, 1fr);
            gap: 20px;
            width: 100%;
        }
        
        /* 移动端 */
        @media (min-width: 576px) {
            .gallery > div.active {
                grid-template-columns: repeat(2, 1fr);
            }
        }
        
        /* 平板 */
        @media (min-width: 768px) {
            .gallery > div.active {
                grid-template-columns: repeat(3, 1fr);
            }
            .container {
                padding: 20px 40px;
            }
        }
        
        /* 小型桌面显示器 */
        @media (min-width: 1024px) {
            .gallery > div.active {
                grid-template-columns: repeat(4, 1fr);
            }
            .item img {
                height: 280px;
            }
        }
        
        /* 中型桌面显示器 */
        @media (min-width: 1440px) {
            .gallery > div.active {
                grid-template-columns: repeat(5, 1fr);
            }
            .item img {
                height: 260px;
            }
        }
        
        /* 大型桌面显示器 */
        @media (min-width: 1920px) {
            .gallery > div.active {
                grid-template-columns: repeat(6, 1fr);
            }
            .item img {
                height: 240px;
            }
        }
        
        .item {
            background: white;
            border-radius: 8px;
            overflow: hidden;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            transition: all 0.3s ease;
            cursor: pointer;
            height: 100%;
            display: flex;
            flex-direction: column;
        }
        
        .item:hover {
            transform: translateY(-5px);
            box-shadow: 0 5px 15px rgba(0,0,0,0.2);
        }
        
        .thumbnail-container {
            position: relative;
            width: 100%;
            padding-top: 100%;
            overflow: hidden;
        }
        
        .item img {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            object-fit: cover;
        }

        .item-footer {
            padding: 15px;
            display: flex;
            flex-direction: column;
            gap: 10px;
            background: white;
        }
        
        .tags {
            display: flex;
            flex-wrap: wrap;
            gap: 5px;
        }
        
        .tag {
            background: #f0f0f0;
            padding: 4px 8px;
            border-radius: 4px;
            font-size: 14px;
        }

        .source-link {
            display: inline-block;
            color: #0066cc;
            text-decoration: none;
            font-size: 14px;
            margin-top: 5px;
        }

        .source-link:hover {
            text-decoration: underline;
        }

        .multi-p-badge {
            position: absolute;
            top: 10px;
            right: 10px;
            background: rgba(0, 0, 0, 0.7);
            color: white;
            padding: 4px 8px;
            border-radius: 4px;
            font-size: 14px;
        }

        .modal {
            display: none;
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0, 0, 0, 0.9);
            z-index: 1000;
            overflow-y: auto;
        }

        .modal.active {
            display: block;
        }

        .modal-content {
            max-width: 1200px;
            margin: 40px auto;
            padding: 20px;
        }

        .modal-close {
            position: fixed;
            top: 20px;
            right: 20px;
            color: white;
            font-size: 30px;
            cursor: pointer;
            background: none;
            border: none;
            width: 40px;
            height: 40px;
            display: flex;
            align-items: center;
            justify-content: center;
            border-radius: 50%;
            background: rgba(0, 0, 0, 0.5);
        }

        .modal img {
            width: 100%;
            height: auto;
            margin-bottom: 20px;
            border-radius: 8px;
        }

        @media (max-width: 768px) {
            .modal-content {
                margin: 20px;
            }
        }
    </style>
</head>
<body>
    <div class="tabs">
        <button class="tab active" onclick="showGallery('daily')">每日</button>
        <button class="tab" onclick="showGallery('weekly')">每周</button>
        <button class="tab" onclick="showGallery('monthly')">每月</button>
        <button class="tab" onclick="showGallery('rookie')">新人</button>
    </div>
    
    <div class="gallery">
'''
    
    # 为每个分类生成图片区域
    for mode, images in data.items():
        html += f'        <div id="{mode}" class="{"active" if mode == "daily" else ""}">\n'
        for img in images:
            # 获取所有图片URL
            img_urls = img['web2url'] if isinstance(img['web2url'], list) else [img['web2url']]
            tags = img['data-tags'].split(' ')
            
            # 生成用于modal的图片数据
            img_data = json.dumps(img_urls).replace('"', '&quot;')
            artwork_id = img.get('data-id', '')
            pixiv_link = f'https://www.pixiv.net/artworks/{artwork_id}' if artwork_id else ''
            
            html += f'''            <div class="item" onclick='showModal({img_data})'>
                <div class="thumbnail-container">
                    <img data-src="{img_urls[0]}" class="lazy">
                    {f'<div class="multi-p-badge">{len(img_urls)}P</div>' if len(img_urls) > 1 else ''}
                </div>
                <div class="item-footer">
                    <div class="tags">
'''
            for tag in tags:
                html += f'                    <span class="tag">{tag}</span>\n'
            html += f'''                </div>
                    <a href="{pixiv_link}" class="source-link" target="_blank" onclick="event.stopPropagation();">查看原帖 ↗</a>
                </div>
            </div>\n'''
        html += '        </div>\n'

    # 添加modal和JavaScript
    html += '''    </div>

    <div class="modal" id="imageModal">
        <button class="modal-close" onclick="closeModal()">×</button>
        <div class="modal-content" id="modalContent">
        </div>
    </div>
    
    <script>
        // 图片加载队列
        const imageQueue = [];
        let isLoading = false;

        // 处理队列中的下一个图片
        function loadNextImage() {
            if (isLoading || imageQueue.length === 0) return;
            
            isLoading = true;
            const img = imageQueue.shift();
            const src = img.getAttribute('data-src');
            
            img.onload = function() {
                img.classList.add('loaded');
                isLoading = false;
                loadNextImage();
            }
            
            img.onerror = function() {
                isLoading = false;
                loadNextImage();
            }
            
            img.src = src;
        }

        // 观察器配置
        const observerOptions = {
            root: null,
            rootMargin: '50px',
            threshold: 0.1
        };

        // 创建观察器
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    if (!img.classList.contains('loaded') && !imageQueue.includes(img)) {
                        imageQueue.push(img);
                        loadNextImage();
                    }
                    observer.unobserve(img);
                }
            });
        }, observerOptions);

        // 初始化懒加载
        document.addEventListener('DOMContentLoaded', function() {
            const lazyImages = document.querySelectorAll('img.lazy');
            lazyImages.forEach(img => observer.observe(img));
        });

        function showGallery(mode) {
            // 更新标签状态
            document.querySelectorAll('.tab').forEach(tab => {
                tab.classList.remove('active');
            });
            document.querySelector(`[onclick="showGallery('${mode}')"]`).classList.add('active');
            
            // 更新图片显示
            document.querySelectorAll('.gallery > div').forEach(div => {
                div.classList.remove('active');
            });
            const activeDiv = document.getElementById(mode);
            activeDiv.classList.add('active');

            // 重新观察新显示的图片
            const newImages = activeDiv.querySelectorAll('img.lazy:not(.loaded)');
            newImages.forEach(img => observer.observe(img));
        }

        function showModal(urls) {
            const modal = document.getElementById('imageModal');
            const content = document.getElementById('modalContent');
            
            // 清空现有内容
            content.innerHTML = '';
            
            // 添加所有图片
            urls.forEach(url => {
                const img = document.createElement('img');
                img.src = url;
                content.appendChild(img);
            });
            
            // 显示modal
            modal.classList.add('active');
            
            // 阻止页面滚动
            document.body.style.overflow = 'hidden';
        }

        function closeModal() {
            const modal = document.getElementById('imageModal');
            modal.classList.remove('active');
            document.body.style.overflow = '';
        }

        // 点击modal背景关闭
        document.getElementById('imageModal').addEventListener('click', function(e) {
            if (e.target === this) {
                closeModal();
            }
        });

        // ESC键关闭modal
        document.addEventListener('keydown', function(e) {
            if (e.key === 'Escape') {
                closeModal();
            }
        });
    </script>
</body>
</html>
'''
    
    # 写入文件
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html)
    
    print("已生成 index.html")

if __name__ == '__main__':
    generate_html() 
    generate_html() 