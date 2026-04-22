import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="My Dashboard", layout="wide")

st.title("📊 My First Dashboard")

# Sidebar
st.sidebar.header("Filters")
choice = st.sidebar.selectbox("Select Option", ["A", "B", "C"])

# Data
data = pd.DataFrame({
    "Days": range(1, 11),
    "Values": np.random.randint(10, 100, 10)
})

# Metrics
col1, col2 = st.columns(2)
col1.metric("Total", data["Values"].sum())
col2.metric("Average", round(data["Values"].mean(), 2))

# Chart
st.line_chart(data.set_index("Days"))

# Table
st.dataframe(data)