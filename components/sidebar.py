import streamlit as st
import datetime
from database.queries import get_unique_regions

def render_sidebar():
    with st.sidebar:
        st.title("⚙️ Filters")
        st.markdown("---")
        
        # Date Filter
        st.subheader("Time Period")
        min_date = datetime.date(2018, 1, 1)
        max_date = datetime.date(2024, 12, 1)
        
        start_date = st.date_input("Start Date", min_value=min_date, max_value=max_date, value=min_date)
        end_date = st.date_input("End Date", min_value=min_date, max_value=max_date, value=max_date)
        
        st.markdown("---")
        
        # Region Filter
        st.subheader("Geography")
        all_regions = get_unique_regions()
        selected_regions = st.multiselect(
            "Select Regions", 
            options=all_regions,
            default=all_regions
        )
        
        st.markdown("---")
        st.info("Economic Insights Dashboard v1.0")
        
        return start_date, end_date, selected_regions
