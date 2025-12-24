import streamlit as st
import os

# --- PAGE SETUP ---
st.set_page_config(
    page_title="BlackMarket Price Spike Intelligence Dashboard",
    page_icon="📈",
    layout="wide"
)

st.title("📊 BlackMarket Price Spike Intelligence Dashboard")
st.markdown("### Live Visualization of Detected Commodity Price Spikes")

# --- VISUALIZATION PATH ---
VIS_DIR = os.path.join(os.getcwd(), "visualizations")

# --- Function to display a visualization file ---
def display_viz(file_name, title):
    file_path = os.path.join(VIS_DIR, file_name)
    if os.path.exists(file_path):
        st.markdown(f"#### {title}")
        with open(file_path, "r", encoding="utf-8") as f:
            html_data = f.read()
            st.components.v1.html(html_data, height=500, scrolling=True)
    else:
        st.warning(f"Visualization '{file_name}' not found.")

# --- DASHBOARD SECTIONS ---
col1, col2 = st.columns(2)

with col1:
    display_viz("commodity_bar.html", "Commodity-wise Average Prices")
    display_viz("market_pie.html", "Market-wise Distribution")

with col2:
    display_viz("top_commodity_line.html", "Price Trend of Top Commodities")
    display_viz("top10_commodities.html", "Top 10 Commodities by Spike Frequency")

st.divider()

display_viz("state_map.html", "State-wise Spike Map")
display_viz("market_commodity_heatmap.html", "Market-Commodity Heatmap")

st.markdown("---")
st.markdown("✅ **Dashboard powered by AI Spike Detection Pipeline**")

