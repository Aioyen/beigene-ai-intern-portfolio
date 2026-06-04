import streamlit as st
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import os, urllib.request

# --- 自动下载中文字体 ---
def setup_chinese_font():
    font_dir = os.path.join(os.path.expanduser("~"), ".fonts")
    font_path = os.path.join(font_dir, "NotoSansSC-Regular.ttf")
    os.makedirs(font_dir, exist_ok=True)
    if not os.path.exists(font_path):
        url = "https://github.com/google/fonts/raw/main/ofl/notosanssc/NotoSansSC%5Bwght%5D.ttf"
        urllib.request.urlretrieve(url, font_path)
    for f in matplotlib.font_manager.fontManager.ttflist:
        if "NotoSansSC" in f.name:
            matplotlib.rcParams["font.sans-serif"] = [f.name, "DejaVu Sans"]
            break
    else:
        matplotlib.font_manager.fontManager.addfont(font_path)
        matplotlib.rcParams["font.sans-serif"] = ["Noto Sans SC", "DejaVu Sans"]
    matplotlib.rcParams["axes.unicode_minus"] = False

setup_chinese_font()

st.set_page_config(page_title="药企数据快速探索工具", layout="wide")
st.title("💊 药企数据快速探索工具")

uploaded = st.file_uploader("上传 Excel 或 CSV 文件", type=["csv", "xlsx", "xls"])

if uploaded is not None:
    if uploaded.name.endswith(".csv"):
        df = pd.read_csv(uploaded)
    else:
        df = pd.read_excel(uploaded)

    st.success(f"已加载 {df.shape[0]} 行 × {df.shape[1]} 列")
    st.subheader("📋 数据预览（前 10 行）")
    st.dataframe(df.head(10), use_container_width=True)

    num_cols = df.select_dtypes(include="number").columns.tolist()
    if len(num_cols) < 2:
        st.warning("至少需要两列数值型数据才能绘制散点图")
    else:
        col1, col2 = st.columns(2)
        with col1:
            x_col = st.selectbox("X 轴", num_cols, index=0)
        with col2:
            y_col = st.selectbox("Y 轴", num_cols, index=min(1, len(num_cols) - 1))

        if st.button("🔍 绘制散点图", type="primary"):
            fig, ax = plt.subplots(figsize=(7, 5))
            ax.scatter(df[x_col], df[y_col], alpha=0.6, edgecolors="white", linewidth=0.5)
            ax.set_xlabel(x_col, fontsize=12)
            ax.set_ylabel(y_col, fontsize=12)
            ax.set_title(f"{x_col} vs {y_col}", fontsize=14, fontweight="bold")
            st.pyplot(fig)
else:
    st.info("👆 请上传一个 Excel 或 CSV 文件开始探索")
