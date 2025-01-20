let currentMode = 'daily';
const gallery = document.querySelector('.gallery');
const navItems = document.querySelectorAll('.nav-item');

async function loadImages(mode) {
    try {
        gallery.innerHTML = '<div class="loading">加载中...</div>';
        const response = await fetch(`/${mode}.json`);
        const images = await response.json();
        
        gallery.innerHTML = '';
        images.forEach(image => {
            const item = document.createElement('div');
            item.className = 'gallery-item';
            
            // 创建图片容器
            const imgContainer = document.createElement('div');
            imgContainer.className = 'gallery-item-img';
            
            // 如果有多张图片，显示第一张
            const imgUrl = Array.isArray(image['web2url']) ? image['web2url'][0] : image['web2url'];
            
            const img = document.createElement('img');
            img.src = imgUrl;
            img.loading = 'lazy';  // 启用懒加载
            imgContainer.appendChild(img);
            
            // 创建标签容器
            const info = document.createElement('div');
            info.className = 'gallery-item-info';
            
            const tags = document.createElement('div');
            tags.className = 'tags';
            const tagList = image['data-tags'].split(' ');
            tagList.forEach(tag => {
                const tagSpan = document.createElement('span');
                tagSpan.className = 'tag';
                tagSpan.textContent = tag;
                tags.appendChild(tagSpan);
            });
            
            info.appendChild(tags);
            
            item.appendChild(imgContainer);
            item.appendChild(info);
            gallery.appendChild(item);
        });
    } catch (error) {
        gallery.innerHTML = '<div class="loading">加载失败，请稍后重试</div>';
        console.error('Error loading images:', error);
    }
}

// 导航切换
navItems.forEach(item => {
    item.addEventListener('click', (e) => {
        e.preventDefault();
        const mode = e.target.dataset.mode;
        if (mode === currentMode) return;
        
        // 更新导航状态
        navItems.forEach(nav => nav.classList.remove('active'));
        e.target.classList.add('active');
        
        // 加载新的图片
        currentMode = mode;
        loadImages(mode);
    });
});

// 初始加载
loadImages(currentMode); 