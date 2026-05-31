import streamlit as st
import pandas as pd
from components.sidebar import render_sidebar
from components.charts import create_choropleth, create_bar_chart
from database.queries import get_macro_data

st.set_page_config(page_title="Regional Comparison", page_icon="🌍", layout="wide")

st.title("🌍 Regional Comparison")

start_date, end_date, selected_regions = render_sidebar()

if not selected_regions:
    st.warning("Please select at least one region from the sidebar.")
    st.stop()

with st.spinner("Generating geographical data..."):
    df = get_macro_data(start_date=start_date, end_date=end_date, regions=selected_regions)

if df is None or df.empty:
    st.error("No data found. Please run `python data/data_generator.py` to seed the database.")
    st.stop()

# Aggregate by country for the selected period
df_country = df.groupby(['country', 'region']).mean(numeric_only=True).reset_index()

st.subheader(f"Global Overview ({start_date.strftime('%Y-%m')} to {end_date.strftime('%Y-%m')})")

tab1, tab2 = st.tabs(["Global Heatmap", "Bar Comparisons"])

with tab1:
    metric = st.selectbox("Select Metric to Visualize", ['GDP Growth', 'Inflation Rate', 'Unemployment Rate'])
    
    col_map = {
        'GDP Growth': 'gdp_growth',
        'Inflation Rate': 'inflation_rate',
        'Unemployment Rate': 'unemployment_rate'
    }
    
    selected_col = col_map[metric]
    
    st.plotly_chart(create_choropleth(df_country, 'country', 'country names', selected_col, f"Average {metric} by Country"), use_container_width=True)

with tab2:
    st.markdown("#### Top Countries by GDP Growth")
    df_sorted = df_country.sort_values(by='gdp_growth', ascending=False)
    st.plotly_chart(create_bar_chart(df_sorted, 'country', 'gdp_growth', 'region', 'Average GDP Growth', 'GDP Growth (%)'), use_container_width=True)
