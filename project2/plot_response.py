import csv
import matplotlib.pyplot as plt
import matplotlib
matplotlib.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei", "DejaVu Sans"]
matplotlib.rcParams["axes.unicode_minus"] = False
from collections import defaultdict

# --- 读取并分组统计 ---
drug_stats = defaultdict(lambda: {"total": 0, "response": 0})

with open("ehr_data.csv", encoding="utf-8-sig") as f:
    for row in csv.DictReader(f):
        drug = row["药物名称"]
        drug_stats[drug]["total"] += 1
        if row["结局"] == "有效":
            drug_stats[drug]["response"] += 1

# --- 计算应答率 ---
drugs = []
rates = []
print("药物应答率：")
for drug, stats in sorted(drug_stats.items()):
    rate = stats["response"] / stats["total"] * 100
    drugs.append(drug)
    rates.append(rate)
    print(f"  {drug}: {stats['response']}/{stats['total']} = {rate:.1f}%")

# --- 画柱状图 ---
colors = ["#4C72B0", "#55A868", "#C44E52"]
plt.figure(figsize=(8, 5))
bars = plt.bar(drugs, rates, color=colors, edgecolor="white", linewidth=0.8)

for bar, rate in zip(bars, rates):
    plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.5,
             f"{rate:.1f}%", ha="center", fontsize=12, fontweight="bold")

plt.ylabel("Response Rate (%)", fontsize=12)
plt.title("Drug Response Rate by Group", fontsize=14, fontweight="bold")
plt.ylim(0, max(rates) * 1.3)
plt.tight_layout()
plt.savefig("response_rate.png", dpi=150)
print("\nDone -> response_rate.png")
