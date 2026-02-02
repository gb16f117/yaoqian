const API_BASE = '/api';

// 摇签按钮
const drawBtn = document.getElementById('drawBtn');
const loadingOverlay = document.getElementById('loadingOverlay');

drawBtn.addEventListener('click', async () => {
    try {
        // 显示加载动画
        loadingOverlay.style.display = 'flex';

        // 调用后端API获取签文
        const response = await fetch(`${API_BASE}/draw`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        });

        const data = await response.json();

        if (response.ok) {
            // 保存签文数据到sessionStorage
            sessionStorage.setItem('currentFortune', JSON.stringify(data));

            // 延迟跳转，让用户看到动画效果
            setTimeout(() => {
                window.location.href = 'result.html';
            }, 2000);
        } else {
            alert('获取签文失败，请重试');
            loadingOverlay.style.display = 'none';
        }
    } catch (error) {
        console.error('摇签失败:', error);
        alert('网络错误，请检查服务器是否启动');
        loadingOverlay.style.display = 'none';
    }
});
