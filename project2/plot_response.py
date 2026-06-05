import csv
import plotly.graph_objects as go
from collections import defaultdict

# --- 读取并分组统计 ---
drug_stats = defaultdict(lambda: {"total": 0, "response": 0})

with open("ehr_data.csv", encoding="utf-8-sig") as f:
    for row in csv.DictReader(f):
        drug = row["药物名称"]
        drug_stats[drug]["total"] += 1
        if row["结局"] == "有效":
            drug_stats[drug]["response"] += 1

# --- 计算应答率 + 准备画图数据 ---
drugs, rates, totals, responses, hover_texts = [], [], [], [], []
print("药物应答率：")
for drug, stats in sorted(drug_stats.items()):
    rate = stats["response"] / stats["total"] * 100
    drugs.append(drug)
    rates.append(round(rate, 1))
    totals.append(stats["total"])
    responses.append(stats["response"])
    hover_texts.append(f"有效率: {rate:.1f}%<br>有效: {stats['response']} / 总例数: {stats['total']}")
    print(f"  {drug}: {stats['response']}/{stats['total']} = {rate:.1f}%")

# --- 用 Plotly 画柱状图 ---
colors = ["#4C72B0", "#55A868", "#C44E52"]
fig = go.Figure()

fig.add_trace(go.Bar(
    x=drugs,
    y=rates,
    marker_color=colors,
    text=[f"{r}%" for r in rates],
    textposition="outside",
    textfont=dict(size=14, family="Microsoft YaHei"),
    hovertext=hover_texts,
    hoverinfo="text",
    hovertemplate="%{hovertext}<extra></extra>",
))

fig.update_layout(
    title=dict(text="药物分组应答率", font=dict(size=18, family="Microsoft YaHei")),
    xaxis=dict(title="药物名称", titlefont=dict(size=14, family="Microsoft YaHei"),
               tickfont=dict(size=13, family="Microsoft YaHei")),
    yaxis=dict(title="应答率 (%)", titlefont=dict(size=14),
               range=[0, max(rates) * 1.3]),
    plot_bgcolor="white",
    width=700,
    height=500,
)

fig.write_html("response_rate.html")
print("\nDone -> response_rate.html")