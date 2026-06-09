# 药物应答率分析

按药物名称分组计算应答率，生成 Plotly 交互柱状图。

## 快速开始

```bash
python plot_response.py
```

## 输入

`ehr_data.csv` — 至少包含「药物名称」「结局」两列（结局列中「有效」计为应答）

## 输出

- **命令行** — 每种药物的应答率和详细计数
- **`response_rate.html`** — 交互式柱状图（浏览器打开，鼠标悬停显示有效例数/总例数）

## 示例

```
药物应答率：
  奥希替尼: 34/173 = 19.7%
  帕博利珠单抗: 26/176 = 14.8%
  阿达木单抗: 29/151 = 19.2%
```

## 技术栈

- `csv` — 读取 EHR 数据
- `plotly.graph_objects` — 柱状图 + `hovertext` 悬停详情
- `collections.defaultdict` — 分组统计

## 依赖

```bash
pip install plotly
```
