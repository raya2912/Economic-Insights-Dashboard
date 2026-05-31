import streamlit as st # Trigger reload
import pandas as pd
import numpy as np
from components.sidebar import render_sidebar
from components.kpi_cards import render_kpi_card
from components.charts import create_line_chart
from database.queries import get_macro_data
from utils.exports import convert_df_to_csv, create_pdf_report

st.set_page_config(page_title="Macro Trends", page_icon="📈", layout="wide")

st.title("📈 Macroeconomic Trends")

start_date, end_date, selected_regions = render_sidebar()

if not selected_regions:
    st.warning("Please select at least one region from the sidebar.")
    st.stop()

with st.spinner("Analyzing macroeconomic indicators..."):
    df = get_macro_data(start_date=start_date, end_date=end_date, regions=selected_regions)

with open("streamlit_debug.txt", "w") as f:
    f.write(f"start_date: {start_date}\n")
    f.write(f"end_date: {end_date}\n")
    f.write(f"regions: {selected_regions}\n")
    f.write(f"df length: {len(df) if df is not None else 'None'}\n")

if df is None or df.empty:
    st.error("No data found. Please run `python data/data_generator.py` to seed the database.")
    st.stop()

# Aggregate Data for KPIs
latest_date = df['date'].max()
prev_date = df[df['date'] < latest_date]['date'].max() if len(df['date'].unique()) > 1 else latest_date

latest_data = df[df['date'] == latest_date].mean(numeric_only=True)
prev_data = df[df['date'] == prev_date].mean(numeric_only=True) if prev_date != latest_date else latest_data

def get_delta(col):
    if prev_date == latest_date or prev_data[col] == 0: return 0
    return round(((latest_data[col] - prev_data[col]) / abs(prev_data[col])) * 100, 2)

st.markdown("### Executive Summary")
col1, col2, col3 = st.columns(3)
with col1:
    render_kpi_card("Average Inflation Rate", f"{latest_data['inflation_rate']:.2f}", get_delta('inflation_rate'), suffix="%")
with col2:
    render_kpi_card("Average GDP Growth", f"{latest_data['gdp_growth']:.2f}", get_delta('gdp_growth'), suffix="%")
with col3:
    render_kpi_card("Average Unemployment", f"{latest_data['unemployment_rate']:.2f}", get_delta('unemployment_rate'), suffix="%")

st.markdown("---")

st.subheader("Time Series Analysis")

tab1, tab2, tab3, tab4 = st.tabs(["Inflation Trends", "GDP Growth", "Unemployment", "🔮 Forecasting"])

df_grouped = df.groupby(['date', 'region']).mean(numeric_only=True).reset_index()

with tab1:
    st.plotly_chart(create_line_chart(df_grouped, 'date', 'inflation_rate', 'region', 'Inflation Rate', 'Inflation (%)'), use_container_width=True)

with tab2:
    st.plotly_chart(create_line_chart(df_grouped, 'date', 'gdp_growth', 'region', 'GDP Growth', 'GDP Growth (%)'), use_container_width=True)

with tab3:
    st.plotly_chart(create_line_chart(df_grouped, 'date', 'unemployment_rate', 'region', 'Unemployment Rate', 'Unemployment (%)'), use_container_width=True)

with tab4:
    st.markdown("#### 6-Month Trend Projection")
    st.caption("Based on simple linear regression of historical data.")
    
    df_global = df.groupby('date').mean(numeric_only=True).reset_index()
    df_global['date_ordinal'] = pd.to_datetime(df_global['date']).apply(lambda date: date.toordinal())
    
    forecast_col = st.selectbox("Select metric to forecast", ["inflation_rate", "gdp_growth", "unemployment_rate"])
    
    if len(df_global) > 2:
        x = df_global['date_ordinal']
        y = df_global[forecast_col]
        z = np.polyfit(x, y, 1)
        p = np.poly1d(z)
        
        future_dates = [latest_date + pd.DateOffset(months=i) for i in range(1, 7)]
        future_ordinals = [d.toordinal() for d in future_dates]
        future_preds = p(future_ordinals)
        
        df_forecast = pd.DataFrame({
            'date': list(df_global['date']) + [d.date() for d in future_dates],
            'Type': ['Historical'] * len(df_global) + ['Forecast'] * 6,
            'Value': list(y) + list(future_preds)
        })
        
        st.plotly_chart(create_line_chart(df_forecast, 'date', 'Value', 'Type', f'{forecast_col.replace("_", " ").title()} Forecast', 'Value'), use_container_width=True)
    else:
        st.info("Not enough data to generate forecast.")

st.markdown("---")
st.subheader("Export Data")
col_exp1, col_exp2 = st.columns([1, 1])

csv = convert_df_to_csv(df)
with col_exp1:
    st.download_button("Download Data as CSV", data=csv, file_name="macro_trends.csv", mime="text/csv")

pdf = create_pdf_report("Macroeconomic Trends Report", df, "This report summarizes the macroeconomic trends based on your current filters.")
with col_exp2:
    st.download_button("Download Report as PDF", data=pdf, file_name="macro_report.pdf", mime="application/pdf")
