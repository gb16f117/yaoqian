const backBtn = document.getElementById('backBtn');
const interpretBtn = document.getElementById('interpretBtn');
const interpretationBox = document.getElementById('interpretationBox');
const footer = document.getElementById('footer');
const source = document.getElementById('source');
const fortuneLevel = document.getElementById('fortuneLevel');
const fortuneName = document.getElementById('fortuneName');
const fortuneText = document.getElementById('fortuneText');
const interpretationText = document.getElementById('interpretationText');

// 获取签文数据
let currentFortune = null;
try {
    const savedFortune = sessionStorage.getItem('currentFortune');
    if (savedFortune) {
        currentFortune = JSON.parse(savedFortune);

        // 显示签文
        fortuneLevel.textContent = currentFortune.level + '签';
        fortuneName.textContent = currentFortune.name;
        fortuneText.innerHTML = currentFortune.content.replace(/\n/g, '<br>');
        interpretationText.textContent = currentFortune.interpretation;

        // 根据签文等级设置不同颜色
        setLevelColor(currentFortune.level);
    } else {
        // 如果没有签文数据，返回首页
        window.location.href = 'index.html';
    }
} catch (error) {
    console.error('获取签文数据失败:', error);
    window.location.href = 'index.html';
}

// 设置签文等级颜色
function setLevelColor(level) {
    const colors = {
        '上上': 'linear-gradient(135deg, #ff6b6b 0%, #feca57 100%)',
        '上中': 'linear-gradient(135deg, #ffa502 0%, #ff7f50 100%)',
        '中上': 'linear-gradient(135deg, #2ed573 0%, #1e90ff 100%)',
        '中中': 'linear-gradient(135deg, #5352ed 0%, #70a1ff 100%)',
        '中下': 'linear-gradient(135deg, #a55eea 0%, #8854d0 100%)'
    };

    fortuneLevel.style.background = colors[level] || colors['中中'];
}

// 返回首页
backBtn.addEventListener('click', () => {
    window.location.href = 'index.html';
});

// 显示解析
interpretBtn.addEventListener('click', () => {
    interpretationBox.style.display = 'block';
    interpretBtn.style.display = 'none';
    source.style.display = 'block';
    footer.style.display = 'block';
});
