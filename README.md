# 摇签小应用

一个专为手机端设计的摇签应用，使用 Flask 后端和原生 HTML 前端，SQLite 数据库存储六十甲子签文。

## 项目结构

```
yaoqian/
├── app.py                    # Flask 后端应用（包含签文数据和API）
├── requirements.txt          # Python 依赖
├── frontend/                # 前端文件
│   ├── index.html          # 摇签页面
│   ├── result.html         # 签文结果页面
│   ├── interpretation.html # 签文解析页面
│   ├── styles.css          # 样式文件
│   ├── app.js              # 摇签页面逻辑
│   ├── result.js           # 结果页面逻辑
│   └── interpretation.js   # 解析页面逻辑
├── fortune.db               # SQLite 数据库（运行时自动生成）
└── README.md               # 项目说明
```

## 功能特性

- 🎲 **随机摇签**：心诚则灵，随机抽取签文
- 📜 **六十甲子签**：完整的60支签文数据
- 🏷️ **签文等级**：上上、上中、中上、中中等不同等级
- 📱 **手机适配**：专为手机端优化，响应式设计
- 🎨 **精美界面**：渐变色背景，流畅动画效果
- 💾 **数据持久化**：SQLite 数据库存储
- 🔄 **页面跳转**：摇签 → 结果 → 解析，流程完整

## 使用流程

1. **摇签页面**：用户点击摇签按钮，显示动画效果
2. **结果页面**：显示抽到的签文等级、名称和签文内容
3. **解析页面**：显示签文的详细解析和运势指引

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 启动后端服务器

```bash
python app.py
```

服务器将在 `http://localhost:5004` 启动，首次运行会自动创建数据库并插入60条签文数据。

### 3. 访问前端

在浏览器中直接打开 `frontend/index.html` 文件

## API 端点

- `GET /api/health` - 健康检查
- `POST /api/draw` - 随机抽取一支签
- `GET /api/fortunes/<id>` - 获取指定签文的详细信息
- `GET /api/fortunes` - 获取所有签文列表

## 签文等级说明

- **上上签**：大吉之兆，所求皆顺
- **上中签**：吉祥之兆，多有贵人相助
- **中上签**：吉兆，稳步前进
- **中中签**：平稳之兆，守成为宜
- **中下签**：需谨慎，耐心等待时机

## 技术栈

**后端:**
- Python 3.x
- Flask
- Flask-CORS
- SQLite

**前端:**
- 原生 HTML5
- 原生 CSS3（渐变、动画、响应式）
- 原生 JavaScript（Fetch API、SessionStorage）

## 开发说明

- 后端服务器运行在 `5000` 端口
- 数据库文件 `fortune.db` 会在首次运行时自动创建
- 前端通过 Fetch API 与后端通信
- 签文数据存储在 sessionStorage 中，页面间共享
- 专为手机端优化，最大宽度 420px

## 注意事项

- 确保后端服务器已启动才能正常摇签
- 前端需要通过 HTTP 协议访问（而非 file://）
- 签文数据在启动时自动插入到数据库
- 刷新页面会丢失当前签文数据

## 许可证

MIT License
