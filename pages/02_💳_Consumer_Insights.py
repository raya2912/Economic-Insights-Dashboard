import streamlit as st
import pandas as pd
from components.sidebar import render_sidebar
from components.kpi_cards import render_kpi_card
from components.charts import create_line_chart
from database.queries import get_consumer_data
from utils.exports import convert_df_to_csv

st.set_page_config(page_title="Consumer Insights", page_icon="💳", layout="wide")

st.title("💳 Consumer Insights")

start_date, end_date, selected_regions = render_sidebar()

if not selected_regions:
    st.warning("Please select at least one region from the sidebar.")
    st.stop()

with st.spinner("Loading consumer data..."):
    df = get_consumer_data(start_date=start_date, end_date=end_date, regions=selected_regions)

if df is None or df.empty:
    st.error("No data found. Please run `python data/data_generator.py` to seed the database.")
    st.stop()

latest_date = df['date'].max()
prev_date = df[df['date'] < latest_date]['date'].max() if len(df['date'].unique()) > 1 else latest_date

latest_data = df[df['date'] == latest_date].mean(numeric_only=True)
prev_data = df[df['date'] == prev_date].mean(numeric_only=True) if prev_date != latest_date else latest_data

def get_delta(col):
    if prev_date == latest_date or prev_data[col] == 0: return 0
    return round(((latest_data[col] - prev_data[col]) / abs(prev_data[col])) * 100, 2)

st.markdown("### Key Metrics")
col1, col2 = st.columns(2)
with col1:
    render_kpi_card("Consumer Spending Index", f"{latest_data['consumer_spending_index']:.1f}", get_delta('consumer_spending_index'))
with col2:
    render_kpi_card("Digital Payment Adoption", f"{latest_data['digital_payment_adoption']:.1f}", get_delta('digital_payment_adoption'), suffix="%")

st.markdown("---")

df_grouped = df.groupby(['date', 'region']).mean(numeric_only=True).reset_index()

st.subheader("Spending Patterns")
st.plotly_chart(create_line_chart(df_grouped, 'date', 'consumer_spending_index', 'region', 'Consumer Spending Index over Time', 'Index Value'), use_container_width=True)

st.subheader("Digital Adoption")
st.plotly_chart(create_line_chart(df_grouped, 'date', 'digital_payment_adoption', 'region', 'Digital Payment Adoption (%)', 'Adoption Rate (%)'), use_container_width=True)

st.markdown("---")
st.download_button("Download Data as CSV", data=convert_df_to_csv(df), file_name="consumer_insights.csv", mime="text/csv")
