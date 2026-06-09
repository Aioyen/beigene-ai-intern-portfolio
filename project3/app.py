import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="药企数据快速探索工具", layout="wide")
st.title("💊 药企数据快速探索工具")

uploaded = st.file_uploader("上传 Excel 或 CSV 文件", type=["csv", "xlsx", "xls"])

if uploaded is not None:
    if uploaded.name.endswith(".csv"):
        df = pd.read_csv(uploaded)
    else:
        df = pd.read_excel(uploaded)

    st.success(f"已加载 {df.shape[0]} 行 x {df.shape[1]} 列")
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
            fig = px.scatter(
                df, x=x_col, y=y_col,
                opacity=0.7,
                title=f"{x_col} vs {y_col}",
                template="simple_white",
            )
            fig.update_traces(marker=dict(size=9, line=dict(width=0.5, color="white")))
            fig.update_layout(height=500)
            st.plotly_chart(fig, use_container_width=True)
else:
    st.info("👆 请上传一个 Excel 或 CSV 文件开始探索")