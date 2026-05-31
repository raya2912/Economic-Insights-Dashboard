import streamlit as st

# Configure the main page
st.set_page_config(
    page_title="Economic Insights Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inject custom CSS for premium fintech aesthetic
st.markdown("""
<style>
    /* Main Background & Text */
    .stApp {
        background-color: #0E1117;
        color: #E0E0E0;
        font-family: 'Inter', sans-serif;
    }
    
    /* Headers */
    h1, h2, h3 {
        color: #FFFFFF;
        font-weight: 600;
    }
    
    /* Top padding adjustment */
    .block-container {
        padding-top: 2rem;
    }

    /* Landing Page Hero Section */
    .hero {
        background: linear-gradient(135deg, #1E1E2D 0%, #151521 100%);
        padding: 40px;
        border-radius: 16px;
        text-align: center;
        border: 1px solid #333;
        box-shadow: 0 10px 20px rgba(0,0,0,0.4);
        margin-bottom: 30px;
    }
    
    .hero h1 {
        font-size: 3rem;
        margin-bottom: 10px;
        background: -webkit-linear-gradient(45deg, #636EFA, #00CC96);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    .hero p {
        font-size: 1.2rem;
        color: #A0A0B0;
    }
</style>
""", unsafe_allow_html=True)

def main():
    st.markdown("""
    <div class="hero">
        <h1>Economic Insights Dashboard</h1>
        <p>A professional analytical platform for tracking macroeconomic and consumer trends globally.</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### 🧭 Navigation")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.info("### 📈 Macro Trends\nAnalyze Inflation, GDP growth, and Unemployment rates across various regions.")
        
    with col2:
        st.success("### 💳 Consumer Insights\nDive deep into Consumer Spending Indices and Digital Payment Adoption.")
        
    with col3:
        st.warning("### 🌍 Regional Comparison\nCompare macroeconomic performance globally using interactive Choropleth maps.")
        
    st.markdown("---")
    st.markdown("👈 **Please select a module from the sidebar to begin your analysis.**")

if __name__ == "__main__":
    main()
