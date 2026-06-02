import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
matplotlib.rcParams["font.sans-serif"] = ["Microsoft YaHei", "SimHei", "DejaVu Sans"]
matplotlib.rcParams["axes.unicode_minus"] = False

st.set_page_config(page_title="药企数据快速探索工具", layout="wide")
st.title("💊 药企数据快速探索工具")

uploaded = st.file_uploader("上传 Excel 或 CSV 文件", type=["csv", "xlsx", "xls"])

if uploaded is not None:
    # 读取文件
    if uploaded.name.endswith(".csv"):
        df = pd.read_csv(uploaded)
    else:
        df = pd.read_excel(uploaded)

    st.success(f"已加载 {df.shape[0]} 行 × {df.shape[1]} 列")

    # 显示前 10 行
    st.subheader("📋 数据预览（前 10 行）")
    st.dataframe(df.head(10), use_container_width=True)

    # 数值列下拉菜单
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
