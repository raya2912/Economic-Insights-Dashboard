import streamlit as st

def render_kpi_card(title, value, delta=None, prefix="", suffix=""):
    """
    Renders a custom styled KPI card using HTML/CSS for a premium look.
    """
    delta_color = "#00CC96" if delta and delta > 0 else "#EF553B"
    delta_arrow = "▲" if delta and delta > 0 else ("▼" if delta and delta < 0 else "-")
    delta_text = f"<span style='color: {delta_color}; font-weight: bold; font-size: 0.9rem;'>{delta_arrow} {abs(delta)}%</span>" if delta is not None else ""

    card_html = f"""
    <div style="
        background: linear-gradient(135deg, #1e1e2d 0%, #151521 100%);
        border: 1px solid #333;
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
        margin-bottom: 20px;
        transition: transform 0.2s ease;
    ">
        <p style="color: #a0a0b0; margin: 0; font-size: 0.9rem; text-transform: uppercase; letter-spacing: 1px;">{title}</p>
        <h2 style="color: #fff; margin: 10px 0 5px 0; font-size: 2.2rem; font-weight: 600;">{prefix}{value}{suffix}</h2>
        {delta_text}
    </div>
    """
    st.markdown(card_html, unsafe_allow_html=True)
