# 药企数据快速探索工具

一个基于 Streamlit 的交互式数据可视化 Web 应用。

## 🌐 在线试用

[https://beigene-ai-intern-portfolio-bv3qvff4bsnpspg9puec2b.streamlit.app/](https://beigene-ai-intern-portfolio-bv3qvff4bsnpspg9puec2b.streamlit.app/)

## 功能

- 📂 上传数据 — 支持 Excel（`.xlsx`/`.xls`）和 CSV
- 📋 数据预览 — 自动显示前 10 行，展示行列数
- 📊 散点图 — 下拉菜单选两个数值列，一键绘图
- 🖱️ 交互悬停 — Plotly 图表，鼠标悬停显示精确数值

## 快速开始

```bash
pip install -r requirements.txt
streamlit run app.py
```

打开 http://localhost:8501。

## Demo

<video src="demo.mp4" controls width="700"></video>

## 技术栈

| 层 | 技术 |
|---|---|
| Web 框架 | Streamlit |
| 数据处理 | Pandas |
| 可视化 | Plotly（交互图表，悬停显示数值） |

## 测试数据

仓库附带 `ehr_test_data.csv`（200 条 x 7 列），包含年龄、BMI、生物标志物等 5 个数值列，可直接用于测试散点图功能。

## 项目结构

```
app.py              # 主应用
requirements.txt    # 依赖
ehr_test_data.csv   # 测试数据
```
