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
col2.metric("Avg Max Temp", f"{df['Predictions'].mean():.1f}°C")
col3.metric("Temp Range", f"{df['Predictions'].min():.0f}°C - {df['Predictions'].max():.0f}°C")

st.markdown("---")

# Weather tiles
st.subheader("Daily Forecast")

cols = st.columns(min(len(df), 7))  # Up to 7 tiles per row

for i, (_, row) in enumerate(df.iterrows()):
    col_idx = i % 7
    icon, label = weather_icon(row['Predictions'])
    
    with cols[col_idx]:
        st.markdown(f"""
        <div style="
            background-color: {'#FFF3E0' if row['Predictions'] > 25 else '#E3F2FD' if row['Predictions'] >= 16 else '#F3E5F5'};
            border-radius: 16px;
            padding: 16px;
            text-align: center;
            margin-bottom: 12px;
        ">
            <div style="font-size: 14px; color: #666;">{row['date'].strftime('%a %d %b')}</div>
            <div style="font-size: 48px; margin: 8px 0;">{icon}</div>
            <div style="font-size: 28px; font-weight: bold; color: #333;">{row['Predictions']:.1f}°C</div>
            <div style="font-size: 14px; color: #888;">{label}</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("---")
st.caption(f"Model: Champion | Updated: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M')}")