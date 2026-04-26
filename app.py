import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.set_page_config(page_title="Sales Dashboard", layout="wide")

st.title("📊 Sales Analytics Dashboard")

# Sidebar Filters
st.sidebar.header("🔍 Filters")
product_filter = st.sidebar.multiselect("Select Products", ["Product A", "Product B", "Product C", "Product D"], default=["Product A", "Product B", "Product C", "Product D"])
region_filter = st.sidebar.selectbox("Select Region", ["All", "North", "South", "East", "West"])
date_range = st.sidebar.slider("Select Date Range", 1, 30, (1, 30))

# Generate sample data
np.random.seed(42)
data = pd.DataFrame({
    "Date": pd.date_range(start="2024-01-01", periods=30, freq='D'),
    "Product": np.random.choice(["Product A", "Product B", "Product C", "Product D"], 30),
    "Region": np.random.choice(["North", "South", "East", "West"], 30),
    "Sales": np.random.randint(1000, 5000, 30),
    "Profit": np.random.randint(100, 800, 30),
    "Units": np.random.randint(50, 200, 30)
})

# Apply filters
filtered_data = data[data["Product"].isin(product_filter)]
if region_filter != "All":
    filtered_data = filtered_data[filtered_data["Region"] == region_filter]
filtered_data = filtered_data[(filtered_data["Date"].dt.day >= date_range[0]) & (filtered_data["Date"].dt.day <= date_range[1])]

# Key Metrics Row
st.subheader("📈 Key Performance Indicators")
col1, col2, col3, col4 = st.columns(4)
col1.metric("💰 Total Sales", f"${filtered_data['Sales'].sum():,.0f}", delta="+12%")
col2.metric("📦 Total Units", f"{filtered_data['Units'].sum():,.0f}", delta="+8%")
col3.metric("💵 Average Profit", f"${filtered_data['Profit'].mean():,.0f}", delta="+5%")
col4.metric("🏆 Profit Margin", f"{(filtered_data['Profit'].sum()/filtered_data['Sales'].sum()*100):.1f}%", delta="+2%")

# Charts Row
col1, col2 = st.columns(2)

with col1:
    st.subheader("📊 Sales by Product (Bar Chart)")
    product_sales = filtered_data.groupby("Product")["Sales"].sum().reset_index()
    fig_bar = px.bar(product_sales, x="Product", y="Sales", color="Product", title="Total Sales Per Product", text="Sales")
    fig_bar.update_traces(texttemplate='$%{text:.0f}', textposition='outside')
    st.plotly_chart(fig_bar, use_container_width=True)

with col2:
    st.subheader("🥧 Sales Distribution (Pie Chart)")
    region_sales = filtered_data.groupby("Region")["Sales"].sum().reset_index()
    fig_pie = px.pie(region_sales, values="Sales", names="Region", title="Sales by Region", hole=0.3)
    st.plotly_chart(fig_pie, use_container_width=True)

# Additional Charts
st.subheader("📉 Sales Trend Over Time")
daily_sales = filtered_data.groupby("Date")["Sales"].sum().reset_index()
fig_line = px.line(daily_sales, x="Date", y="Sales", title="Daily Sales Trend", markers=True)
st.plotly_chart(fig_line, use_container_width=True)

# Data Tables
tab1, tab2 = st.tabs(["📋 Raw Data", "📊 Summary Statistics"])
with tab1:
    st.dataframe(filtered_data, use_container_width=True)
with tab2:
    st.dataframe(filtered_data.describe(), use_container_width=True)

# Download Button
csv = filtered_data.to_csv(index=False)
st.download_button(label="📥 Download Data as CSV", data=csv, file_name="sales_data.csv", mime="text/csv")
