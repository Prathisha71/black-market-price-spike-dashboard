# visualizations.py
import pandas as pd
import plotly.express as px
import streamlit as st
from db_config import get_db_connection

# Load Data

@st.cache_data
def get_spikes():
    """Fetch spike data from the price_spikes table."""
    conn = get_db_connection()
    spikes_df = pd.read_sql_query("SELECT * FROM price_spikes", conn)
    conn.close()
    # Convert date to datetime
    if not spikes_df.empty:
        spikes_df['date'] = pd.to_datetime(spikes_df['date'])
    return spikes_df

# Visualization Functions

def commodity_spike_bar(spikes_df):
    df = spikes_df.groupby("commodity")["spike_percent"].mean().reset_index()
    fig = px.bar(
        df,
        x="commodity",
        y="spike_percent",
        color="spike_percent",
        color_continuous_scale="Reds",
        title="📊 Average Spike % per Commodity",
    )
    return fig

def market_spike_pie(spikes_df):
    df = spikes_df.groupby("market").size().reset_index(name="count")
    fig = px.pie(
        df,
        names="market",
        values="count",
        title="🥧 Spike Distribution Across Markets",
    )
    return fig

def top10_commodities_spikes(spikes_df):
    df = (
        spikes_df.groupby("commodity")["spike_percent"]
        .mean()
        .sort_values(ascending=False)
        .head(10)
        .reset_index()
    )
    fig = px.bar(
        df,
        x="commodity",
        y="spike_percent",
        color="spike_percent",
        color_continuous_scale="Oranges",
        title="🏆 Top 10 Commodities by Spike %",
    )
    return fig

def top_markets_for_top_commodity(spikes_df, top_commodity):
    df = spikes_df[spikes_df["commodity"] == top_commodity]
    df = df.groupby("market")["spike_percent"].mean().sort_values(ascending=False).reset_index()
    fig = px.bar(
        df,
        x="market",
        y="spike_percent",
        color="spike_percent",
        color_continuous_scale="Blues",
        title=f"📊 Top Markets for {top_commodity} by Average Spike %"
    )
    return fig

def state_wise_spike_map(spikes_df):
    """Map showing spike counts per country/state"""
    if "country" not in spikes_df.columns:
        spikes_df["country"] = "India"

    df_grouped = spikes_df.groupby("country").agg(
        spike_count=("spike_percent", "count"),
        spike_avg=("spike_percent", "mean")
    ).reset_index()

    fig = px.choropleth(
        df_grouped,
        locations="country",
        locationmode="country names",
        color="spike_count",
        hover_name="country",
        hover_data={"spike_count": True, "spike_avg": ":.2f"},
        color_continuous_scale="Reds",
        title="🌎 Spike Count per Country/State"
    )
    fig.update_layout(geo=dict(showframe=False, showcoastlines=True))
    return fig

def market_commodity_heatmap(spikes_df):
    heatmap_data = spikes_df.pivot_table(
        index="market",
        columns="commodity",
        values="spike_percent",
        aggfunc="mean",
        fill_value=0,
    )
    fig = px.imshow(
        heatmap_data,
        text_auto=True,
        aspect="auto",
        title="🔥 Heatmap of Market vs Commodity Spikes",
    )
    return fig

# -----------------------------
# Advanced Visualizations
# -----------------------------
def spike_severity_pie(spikes_df):
    df = spikes_df.groupby("alert_level").size().reset_index(name="count")
    fig = px.pie(
        df,
        names="alert_level",
        values="count",
        color="alert_level",
        color_discrete_map={"High": "red", "Medium": "orange", "Low": "green"},
        title="⚡ Spike Severity Distribution"
    )
    return fig

def spike_trend_over_time(spikes_df):
    df = spikes_df.copy()
    df['month'] = df['date'].dt.to_period('M')
    df_grouped = df.groupby('month')['spike_percent'].mean().reset_index()
    df_grouped['month'] = df_grouped['month'].astype(str)
    fig = px.line(
        df_grouped,
        x='month',
        y='spike_percent',
        markers=True,
        title="📈 Average Spike Trend Over Time"
    )
    return fig

def commodity_severity_heatmap(spikes_df):
    df = spikes_df.pivot_table(
        index="commodity",
        columns="alert_level",
        values="spike_percent",
        aggfunc="mean",
        fill_value=0
    )
    fig = px.imshow(
        df,
        text_auto=True,
        aspect="auto",
        color_continuous_scale="RdYlGn_r",
        title="🔥 Commodity vs Spike Severity Heatmap"
    )
    return fig

def top_states_by_spike(spikes_df):
    df = spikes_df.groupby("state")["spike_percent"].mean().sort_values(ascending=False).reset_index()
    fig = px.bar(
        df,
        x="state",
        y="spike_percent",
        color="spike_percent",
        color_continuous_scale="Purples",
        title="🏆 Top States by Average Spike %"
    )
    return fig

def spike_count_per_market(spikes_df):
    df = spikes_df.groupby("market").size().sort_values(ascending=False).reset_index(name="count")
    fig = px.bar(
        df,
        x="count",
        y="market",
        orientation="h",
        color="count",
        color_continuous_scale="Viridis",
        title="📊 Spike Count per Market"
    )
    return fig

# -----------------------------
# New Additional Advanced Visualizations
# -----------------------------
def commodity_box_plot(spikes_df):
    fig = px.box(
        spikes_df,
        x="commodity",
        y="spike_percent",
        color="commodity",
        title="📦 Commodity Spike % Distribution (Box Plot)",
        points="all"
    )
    return fig

def market_spike_scatter(spikes_df):
    severity_color = {"High": "red", "Medium": "orange", "Low": "green"}
    
    df = spikes_df.copy()
    df['size_spike'] = df['spike_percent'].abs()  # fix negative size error
    
    fig = px.scatter(
        df,
        x="market",
        y="spike_percent",
        size="size_spike",
        color="alert_level",
        color_discrete_map=severity_color,
        hover_data=["commodity", "date"],
        title="🔍 Market vs Spike % Scatter (Size=Spike%, Color=Severity)"
    )
    return fig

def monthly_spike_heatmap(spikes_df):
    df = spikes_df.copy()
    df['month'] = df['date'].dt.to_period('M')
    df_grouped = df.pivot_table(
        index="month",
        columns="commodity",
        values="spike_percent",
        aggfunc="mean",
        fill_value=0
    )
    df_grouped.index = df_grouped.index.astype(str)
    fig = px.imshow(
        df_grouped,
        text_auto=True,
        aspect="auto",
        color_continuous_scale="Viridis",
        title="📅 Monthly Average Spike Heatmap"
    )
    return fig

def cumulative_spikes_timeline(spikes_df):
    df = spikes_df.copy().sort_values("date")
    df['cumulative_spikes'] = df['spike_percent'].cumsum()
    fig = px.line(
        df,
        x="date",
        y="cumulative_spikes",
        title="📈 Cumulative Spikes Over Time",
        markers=True
    )
    return fig

# -----------------------------------
# Streamlit Dashboard
# -----------------------------------
def main():
    st.set_page_config(page_title="Black Market Price Spike Dashboard", layout="wide")
    st.title("💹 Black Market Price Spike Analysis Dashboard")

    spikes_df = get_spikes()
    if spikes_df.empty:
        st.warning("⚠ No spike data found. Please run anomaly detection first.")
        return

    # Top commodity
    top_commodity = spikes_df.groupby("commodity")["spike_percent"].mean().idxmax()

    # KPI Section
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Spikes", len(spikes_df))
    col2.metric("Unique Commodities", spikes_df["commodity"].nunique())
    col3.metric("Top Commodity", top_commodity)

    # Existing charts
    st.subheader("📊 Commodity and Market Analysis")
    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(commodity_spike_bar(spikes_df), use_container_width=True)
    with col2:
        st.plotly_chart(market_spike_pie(spikes_df), use_container_width=True)

    st.subheader(f"📊 Top Markets for {top_commodity}")
    st.plotly_chart(top_markets_for_top_commodity(spikes_df, top_commodity), use_container_width=True)

    st.subheader("🏆 Top 10 Commodities by Spike %")
    st.plotly_chart(top10_commodities_spikes(spikes_df), use_container_width=True)

    st.subheader("🗺 State and Market Insights")
    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(state_wise_spike_map(spikes_df), use_container_width=True)
    with col2:
        st.plotly_chart(market_commodity_heatmap(spikes_df), use_container_width=True)

    # Advanced Visualizations
    st.subheader("⚡ Spike Severity Distribution")
    st.plotly_chart(spike_severity_pie(spikes_df), use_container_width=True)

    st.subheader("📈 Spike Trend Over Time")
    st.plotly_chart(spike_trend_over_time(spikes_df), use_container_width=True)

    st.subheader("🔥 Commodity vs Spike Severity Heatmap")
    st.plotly_chart(commodity_severity_heatmap(spikes_df), use_container_width=True)

    st.subheader("🏆 Top States by Average Spike %")
    st.plotly_chart(top_states_by_spike(spikes_df), use_container_width=True)

    st.subheader("📊 Spike Count per Market")
    st.plotly_chart(spike_count_per_market(spikes_df), use_container_width=True)

    # New Interactive Plots
    st.subheader("📦 Commodity Spike Distribution (Box Plot)")
    st.plotly_chart(commodity_box_plot(spikes_df), use_container_width=True)

    st.subheader("🔍 Market vs Spike % Scatter")
    st.plotly_chart(market_spike_scatter(spikes_df), use_container_width=True)

    st.subheader("📅 Monthly Average Spike Heatmap")
    st.plotly_chart(monthly_spike_heatmap(spikes_df), use_container_width=True)

    st.subheader("📈 Cumulative Spikes Timeline")
    st.plotly_chart(cumulative_spikes_timeline(spikes_df), use_container_width=True)


if __name__ == "__main__":
    main()
