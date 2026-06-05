# 💊 药企数据快速探索工具

一个基于 Streamlit 的轻量级数据可视化 Web 应用，上传 Excel 或 CSV 即可快速预览和探索数据。

## 🎬 Demo

<video src="demo.mp4" controls width="700"></video>

## 🚀 功能

- 📂 上传 Excel (`.xlsx`/`.xls`) 或 CSV 文件
- 📋 自动显示数据前 10 行预览
- 📊 下拉菜单选择任意两个数值列，一键绘制散点图
- 🌐 纯浏览器操作，无需本地安装 Python

## 🛠️ 技术栈

- **Streamlit** — Web 框架
- **Pandas** — 数据处理
- **Matplotlib** — 可视化

## 🏃 快速开始

```bash
# 安装依赖
pip install -r requirements.txt

# 启动应用
streamlit run app.py
```

打开 http://localhost:8501 即可使用。
