import streamlit as st
import pandas as pd

st.set_page_config(page_title="Max Temp Forecast", layout="wide")
st.title("🌤️ Maximum Temperature Forecast")

# Load predictions
df = pd.read_csv('weather_data/data/Predictions.csv', parse_dates=['date'])
df = df.sort_values('date')

# Weather icon logic
def weather_icon(temp):
    if temp > 25:
        return "☀️", "Hot"
    elif temp >= 16:
        return "🌤️", "Mild"
    else:
        return "🌡️", "Cool"

# Metrics row
col1, col2, col3 = st.columns(3)
col1.metric("Forecast Days", len(df))
col2.metric("Avg Max Temp", f"{df['Optimized Predictions'].mean():.1f}°C")
col3.metric("Temp Range", f"{df['Optimized Predictions'].min():.0f}°C - {df['Optimized Predictions'].max():.0f}°C")

st.markdown("---")

# Weather tiles — clean grid
st.subheader("Daily Forecast")

# Use fixed 7 columns on desktop, Streamlit handles mobile stacking
cols = st.columns(7)

for i, (_, row) in enumerate(df.iterrows()):
    temp = row['Optimized Predictions']
    interval = row['95 Interval limit']
    icon, label = weather_icon(temp)

    with cols[i % 7]:
        st.markdown(f"""
        <div style="
            background-color: {'#FFF3E0' if temp > 25 else '#E3F2FD' if temp >= 16 else '#F3E5F5'};
            border-radius: 12px;
            padding: 12px 8px;
            text-align: center;
            margin-bottom: 8px;
        ">
            <div style="font-size: 13px; color: #666;">{row['date'].strftime('%a')}</div>
            <div style="font-size: 11px; color: #999;">{row['date'].strftime('%d %b')}</div>
            <div style="font-size: 32px; margin: 4px 0;">{icon}</div>
            <div style="font-size: 20px; font-weight: bold; color: #333;">{temp:.0f}°C</div>
            <div style="font-size: 11px; color: #888;">{label}</div>
            <div style="font-size: 12px; color: #555; margin-top: 2px;">
                {temp - interval:.0f}°–{temp + interval:.0f}°
            </div>
        </div>
        """, unsafe_allow_html=True)

    # Start a new row every 7 tiles
    if (i + 1) % 7 == 0 and (i + 1) < len(df):
        st.markdown("<br>", unsafe_allow_html=True)
        cols = st.columns(7)

st.markdown("---")
st.caption(f"Model: Champion | Updated: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M')}")