import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="TempCast | Maximum Temperature Forecast",
    page_icon="🌤️",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# ============================================================
# LOAD DATA
# ============================================================

@st.cache_data
def load_data():
    df = pd.read_csv(
        "weather_data/data/Predictions.csv",
        parse_dates=["date"]
    )

    df = df.sort_values("date").reset_index(drop=True)

    df["prediction"] = df["Optimized Predictions"]
    df["interval"] = df["95 Interval Limit"]

    df["lower"] = df["prediction"] - df["interval"]
    df["upper"] = df["prediction"] + df["interval"]

    return df


df = load_data()


# ============================================================
# THEME
# ============================================================

if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = False

theme_col1, theme_col2, theme_col3 = st.columns([6, 1, 1])

with theme_col3:
    if st.button(
        "🌙" if not st.session_state.dark_mode else "☀️",
        key="theme_toggle",
        help="Toggle light / dark mode"
    ):
        st.session_state.dark_mode = not st.session_state.dark_mode
        st.rerun()


dark = st.session_state.dark_mode


# ============================================================
# COLOURS
# ============================================================

if dark:

    BG = "#0B1120"
    CARD = "#111827"
    CARD_ALT = "#172033"
    TEXT = "#F8FAFC"
    MUTED = "#94A3B8"
    BORDER = "#263449"
    ACCENT = "#60A5FA"
    GRAPH = "#60A5FA"
    GRID = "#1E293B"

else:

    BG = "#F5F7FB"
    CARD = "#FFFFFF"
    CARD_ALT = "#F8FAFC"
    TEXT = "#111827"
    MUTED = "#64748B"
    BORDER = "#E2E8F0"
    ACCENT = "#2563EB"
    GRAPH = "#2563EB"
    GRID = "#E2E8F0"


# ============================================================
# GLOBAL CSS
# ============================================================

st.markdown(
    f"""
    <style>

    /* Main background */

    .stApp {{
        background: {BG};
        color: {TEXT};
    }}

    .main .block-container {{
        max-width: 1400px;
        padding-top: 1.5rem;
        padding-bottom: 3rem;
    }}

    /* Hide Streamlit chrome */

    #MainMenu {{
        visibility: hidden;
    }}

    footer {{
        visibility: hidden;
    }}

    header {{
        visibility: hidden;
    }}

    /* Buttons */

    .stButton > button {{
        border-radius: 12px;
        border: 1px solid {BORDER};
        background: {CARD};
        color: {TEXT};
        transition: all 0.2s ease;
    }}

    .stButton > button:hover {{
        border-color: {ACCENT};
        color: {ACCENT};
        transform: translateY(-1px);
    }}

    /* Metric cards */

    div[data-testid="stMetric"] {{
        background: {CARD};
        border: 1px solid {BORDER};
        border-radius: 18px;
        padding: 18px;
    }}

    div[data-testid="stMetricLabel"] {{
        color: {MUTED};
    }}

    div[data-testid="stMetricValue"] {{
        color: {TEXT};
    }}

    /* Dialog */

    div[data-testid="stDialog"] > div {{
        background: {CARD};
        border-radius: 24px;
    }}

    /* Mobile */

    @media (max-width: 768px) {{

        .main .block-container {{
            padding-left: 1rem;
            padding-right: 1rem;
        }}

    }}

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# WEATHER LOGIC
# ============================================================

def weather_info(temp):

    if temp > 30:
        return (
            "🥵",
            "Very Hot",
            "Stay hydrated and avoid prolonged exposure to the midday heat."
        )

    elif temp > 25:
        return (
            "☀️",
            "Hot",
            "Great for summer clothes. Sunscreen and water are a good idea."
        )

    elif temp >= 21:
        return (
            "😎",
            "Warm",
            "Comfortable weather. Light clothing should be enough."
        )

    elif temp >= 16:
        return (
            "🌤️",
            "Mild",
            "Pleasant conditions. A light layer may be useful."
        )

    elif temp >= 10:
        return (
            "🌥️",
            "Cool",
            "You may want a jacket, especially later in the day."
        )

    else:
        return (
            "🥶",
            "Cold",
            "Bundle up. A proper jacket or coat is recommended."
        )


def get_recommendations(temp):

    recommendations = []

    if temp > 30:
        recommendations.extend([
            ("💧", "Stay hydrated"),
            ("🧴", "Use sunscreen"),
            ("🕶️", "Sunglasses recommended"),
            ("👕", "Wear light clothing"),
            ("🌳", "Seek shade during peak heat")
        ])

    elif temp > 25:
        recommendations.extend([
            ("🧴", "Sunscreen is a good idea"),
            ("💧", "Take some water"),
            ("🕶️", "Sunglasses recommended"),
            ("👕", "Light clothing should be comfortable")
        ])

    elif temp >= 21:
        recommendations.extend([
            ("😎", "Great T-shirt weather"),
            ("💧", "Stay hydrated"),
            ("🕶️", "Sunglasses could come in handy")
        ])

    elif temp >= 16:
        recommendations.extend([
            ("👕", "Light clothing should work"),
            ("🧥", "A light layer may be useful"),
            ("🚶", "Nice conditions for being outdoors")
        ])

    elif temp >= 10:
        recommendations.extend([
            ("🧥", "Bring a jacket"),
            ("👟", "Good weather for a walk"),
            ("☕", "Potentially excellent coffee weather")
        ])

    else:
        recommendations.extend([
            ("🧥", "Wear a warm jacket"),
            ("🧣", "Consider an extra layer"),
            ("☕", "Hot drink weather")
        ])

    return recommendations


# ============================================================
# HEADER
# ============================================================

first_temp = df.iloc[0]["prediction"]
first_icon, first_label, _ = weather_info(first_temp)

st.markdown(
    f"""
    <div style="
        padding: 10px 0 30px 0;
    ">

        <div style="
            font-size: 15px;
            color: {ACCENT};
            font-weight: 700;
            letter-spacing: 1px;
            text-transform: uppercase;
            margin-bottom: 8px;
        ">
            TEMPERATURE FORECAST
        </div>

        <div style="
            font-size: clamp(38px, 5vw, 64px);
            font-weight: 800;
            letter-spacing: -2px;
            line-height: 1.05;
            color: {TEXT};
        ">
            Maximum temperature,<br>
            predicted.
        </div>

        <div style="
            font-size: 18px;
            color: {MUTED};
            margin-top: 14px;
            max-width: 650px;
        ">
            A probabilistic two-week temperature forecast powered by
            the Champion model.
        </div>

    </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# HERO FORECAST
# ============================================================

hero_col1, hero_col2 = st.columns([2, 1])

with hero_col1:

    st.markdown(
        f"""
        <div style="
            background: linear-gradient(
                135deg,
                {'#172554' if dark else '#DBEAFE'},
                {'#1E3A8A' if dark else '#EFF6FF'}
            );
            border: 1px solid {BORDER};
            border-radius: 26px;
            padding: 32px;
            min-height: 260px;
        ">

            <div style="
                color: {MUTED};
                font-size: 15px;
                font-weight: 600;
            ">
                NEXT FORECAST
            </div>

            <div style="
                margin-top: 20px;
                font-size: 20px;
                color: {TEXT};
            ">
                {df.iloc[0]["date"].strftime("%A, %d %B")}
            </div>

            <div style="
                display: flex;
                align-items: center;
                gap: 18px;
                margin-top: 4px;
            ">

                <div style="font-size: 65px;">
                    {first_icon}
                </div>

                <div style="
                    font-size: 64px;
                    font-weight: 800;
                    color: {TEXT};
                    letter-spacing: -3px;
                ">
                    {first_temp:.0f}°
                </div>

            </div>

            <div style="
                font-size: 18px;
                color: {MUTED};
                margin-top: -4px;
            ">
                {first_label}
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


with hero_col2:

    hottest = df.loc[df["prediction"].idxmax()]
    coldest = df.loc[df["prediction"].idxmin()]

    st.markdown(
        f"""
        <div style="
            background: {CARD};
            border: 1px solid {BORDER};
            border-radius: 26px;
            padding: 26px;
            min-height: 260px;
        ">

            <div style="
                color: {MUTED};
                font-size: 13px;
                font-weight: 700;
                text-transform: uppercase;
            ">
                TWO WEEK OUTLOOK
            </div>

            <div style="
                margin-top: 22px;
                font-size: 15px;
                color: {MUTED};
            ">
                Warmest day
            </div>

            <div style="
                font-size: 28px;
                font-weight: 800;
                color: {TEXT};
            ">
                ☀️ {hottest["prediction"]:.0f}°C
            </div>

            <div style="
                color: {MUTED};
                font-size: 13px;
            ">
                {hottest["date"].strftime("%A, %d %b")}
            </div>

            <div style="
                margin-top: 18px;
                font-size: 15px;
                color: {MUTED};
            ">
                Coolest day
            </div>

            <div style="
                font-size: 28px;
                font-weight: 800;
                color: {TEXT};
            ">
                🥶 {coldest["prediction"]:.0f}°C
            </div>

            <div style="
                color: {MUTED};
                font-size: 13px;
            ">
                {coldest["date"].strftime("%A, %d %b")}
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


st.markdown("<div style='height: 28px'></div>", unsafe_allow_html=True)


# ============================================================
# KEY METRICS
# ============================================================

avg_temp = df["prediction"].mean()
temp_min = df["prediction"].min()
temp_max = df["prediction"].max()

m1, m2, m3, m4 = st.columns(4)

m1.metric(
    "Forecast days",
    f"{len(df)}"
)

m2.metric(
    "Average maximum",
    f"{avg_temp:.1f}°C"
)

m3.metric(
    "Warmest",
    f"{temp_max:.0f}°C"
)

m4.metric(
    "Coolest",
    f"{temp_min:.0f}°C"
)


st.markdown("<div style='height: 35px'></div>", unsafe_allow_html=True)


# ============================================================
# FORECAST GRAPH
# ============================================================

st.markdown(
    f"""
    <div style="
        font-size: 27px;
        font-weight: 750;
        color: {TEXT};
        margin-bottom: 3px;
    ">
        Temperature outlook
    </div>

    <div style="
        font-size: 15px;
        color: {MUTED};
        margin-bottom: 15px;
    ">
        Predicted maximum temperature and 95% prediction interval
    </div>
    """,
    unsafe_allow_html=True
)


fig = go.Figure()


# Confidence interval

fig.add_trace(
    go.Scatter(
        x=pd.concat([df["date"], df["date"][::-1]]),
        y=pd.concat([df["upper"], df["lower"][::-1]]),
        fill="toself",
        fillcolor=(
            "rgba(96,165,250,0.15)"
            if dark
            else "rgba(37,99,235,0.10)"
        ),
        line=dict(color="rgba(255,255,255,0)"),
        hoverinfo="skip",
        name="95% prediction interval"
    )
)


# Prediction line

fig.add_trace(
    go.Scatter(
        x=df["date"],
        y=df["prediction"],
        mode="lines+markers",
        line=dict(
            color=GRAPH,
            width=4,
            shape="spline"
        ),
        marker=dict(
            size=8,
            color=GRAPH
        ),
        name="Predicted maximum",
        customdata=df[["lower", "upper"]].values,
        hovertemplate=(
            "<b>%{x|%A, %d %b}</b><br>"
            "Predicted: <b>%{y:.1f}°C</b><br>"
            "95% range: %{customdata[0]:.1f}°C – "
            "%{customdata[1]:.1f}°C"
            "<extra></extra>"
        )
    )
)


fig.update_layout(
    height=420,
    margin=dict(l=10, r=10, t=20, b=10),
    paper_bgcolor=CARD,
    plot_bgcolor=CARD,
    font=dict(
        color=TEXT,
        family="Inter, Arial"
    ),
    xaxis=dict(
        showgrid=False,
        tickformat="%a\n%d %b",
        linecolor=BORDER
    ),
    yaxis=dict(
        title="°C",
        gridcolor=GRID,
        zeroline=False
    ),
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1
    ),
    hoverlabel=dict(
        bgcolor=CARD,
        font_color=TEXT
    )
)


st.plotly_chart(
    fig,
    use_container_width=True,
    config={
        "displayModeBar": False,
        "responsive": True
    }
)


# ============================================================
# FORECAST SUMMARY
# ============================================================

first_prediction = df.iloc[0]["prediction"]
last_prediction = df.iloc[-1]["prediction"]

difference = last_prediction - first_prediction

if difference > 2:
    trend_text = (
        f"Temperatures are expected to trend warmer, "
        f"rising by roughly {difference:.1f}°C across the forecast."
    )
elif difference < -2:
    trend_text = (
        f"Temperatures are expected to trend cooler, "
        f"falling by roughly {abs(difference):.1f}°C across the forecast."
    )
else:
    trend_text = (
        "Temperatures look relatively stable across the forecast period."
    )


st.markdown(
    f"""
    <div style="
        background: {CARD};
        border: 1px solid {BORDER};
        border-radius: 20px;
        padding: 20px 24px;
        margin: 5px 0 35px 0;
    ">

        <div style="
            font-size: 13px;
            color: {ACCENT};
            font-weight: 700;
            text-transform: uppercase;
        ">
            FORECAST STORY
        </div>

        <div style="
            font-size: 18px;
            color: {TEXT};
            font-weight: 600;
            margin-top: 7px;
        ">
            {trend_text}
        </div>

    </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# DAILY FORECAST
# ============================================================

st.markdown(
    f"""
    <div style="
        font-size: 27px;
        font-weight: 750;
        color: {TEXT};
    ">
        Daily forecast
    </div>

    <div style="
        font-size: 15px;
        color: {MUTED};
        margin-bottom: 20px;
    ">
        Tap a day to see what the temperature means for you.
    </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# DAY DETAIL DIALOG
# ============================================================

@st.dialog("Daily forecast")
def show_day_details(row):

    temp = row["prediction"]
    icon, label, description = weather_info(temp)

    st.markdown(
        f"""
        <div style="
            text-align:center;
            padding: 5px 0 20px 0;
        ">

            <div style="font-size: 60px;">
                {icon}
            </div>

            <div style="
                font-size: 15px;
                color: {MUTED};
            ">
                {row["date"].strftime("%A, %d %B %Y")}
            </div>

            <div style="
                font-size: 52px;
                font-weight: 800;
                color: {TEXT};
                margin-top: 4px;
            ">
                {temp:.0f}°C
            </div>

            <div style="
                font-size: 18px;
                color: {ACCENT};
                font-weight: 650;
            ">
                {label}
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        f"""
        <div style="
            background: {CARD_ALT};
            border: 1px solid {BORDER};
            border-radius: 16px;
            padding: 16px;
            margin-bottom: 20px;
        ">

            <div style="
                font-size: 13px;
                color: {MUTED};
                font-weight: 700;
            ">
                MODEL PREDICTION RANGE
            </div>

            <div style="
                font-size: 25px;
                font-weight: 750;
                color: {TEXT};
                margin-top: 4px;
            ">
                {row["lower"]:.0f}° — {row["upper"]:.0f}°C
            </div>

            <div style="
                font-size: 12px;
                color: {MUTED};
                margin-top: 3px;
            ">
                95% prediction interval
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        f"""
        <div style="
            font-size: 16px;
            color: {TEXT};
            margin-bottom: 15px;
        ">
            {description}
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        f"""
        <div style="
            font-size: 16px;
            font-weight: 700;
            color: {TEXT};
            margin-bottom: 12px;
        ">
            What should you do?
        </div>
        """,
        unsafe_allow_html=True
    )

    recommendations = get_recommendations(temp)

    for emoji, recommendation in recommendations:

        st.markdown(
            f"""
            <div style="
                display:flex;
                align-items:center;
                gap:12px;
                background:{CARD_ALT};
                border:1px solid {BORDER};
                border-radius:12px;
                padding:10px 13px;
                margin-bottom:8px;
                color:{TEXT};
            ">
                <span style="font-size:20px;">{emoji}</span>
                <span>{recommendation}</span>
            </div>
            """,
            unsafe_allow_html=True
        )


# ============================================================
# DAILY CARDS
# ============================================================

# Seven columns per row

for start in range(0, len(df), 7):

    row_df = df.iloc[start:start + 7]

    columns = st.columns(7)

    for column, (_, row) in zip(columns, row_df.iterrows()):

        temp = row["prediction"]
        icon, label, _ = weather_info(temp)

        # Temperature-based card background

        if temp > 30:

            card_bg = (
                "#451A03" if dark
                else "#FFF7ED"
            )

            accent = "#F97316"

        elif temp > 25:

            card_bg = (
                "#422006" if dark
                else "#FFF7ED"
            )

            accent = "#F59E0B"

        elif temp >= 16:

            card_bg = (
                "#172554" if dark
                else "#EFF6FF"
            )

            accent = "#3B82F6"

        else:

            card_bg = (
                "#2E1065" if dark
                else "#F5F3FF"
            )

            accent = "#8B5CF6"

        with column:

            # Unique button label

            button_label = (
                f"{icon}  {temp:.0f}°C\n"
                f"{row['date'].strftime('%a %d')}"
            )

            clicked = st.button(
                button_label,
                key=f"day_{start}_{row['date']}",
                use_container_width=True
            )

            # Card underneath the button

            st.markdown(
                f"""
                <div style="
                    background:{card_bg};
                    border:1px solid {BORDER};
                    border-radius:18px;
                    padding:12px 8px;
                    margin-top:-8px;
                    margin-bottom:25px;
                    text-align:center;
                    pointer-events:none;
                ">

                    <div style="
                        font-size:11px;
                        color:{MUTED};
                        text-transform:uppercase;
                        font-weight:700;
                    ">
                        {row["date"].strftime("%a")}
                    </div>

                    <div style="
                        font-size:11px;
                        color:{MUTED};
                        margin-top:2px;
                    ">
                        {row["date"].strftime("%d %b")}
                    </div>

                    <div style="
                        font-size:32px;
                        margin:7px 0;
                    ">
                        {icon}
                    </div>

                    <div style="
                        font-size:25px;
                        font-weight:800;
                        color:{TEXT};
                    ">
                        {temp:.0f}°
                    </div>

                    <div style="
                        font-size:11px;
                        color:{accent};
                        font-weight:700;
                        margin-top:2px;
                    ">
                        {label}
                    </div>

                    <div style="
                        font-size:11px;
                        color:{MUTED};
                        margin-top:8px;
                    ">
                        {row["lower"]:.0f}° – {row["upper"]:.0f}°
                    </div>

                </div>
                """,
                unsafe_allow_html=True
            )

            if clicked:
                show_day_details(row)


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    f"""
    <div style="
        border-top:1px solid {BORDER};
        margin-top:30px;
        padding-top:20px;
        text-align:center;
        color:{MUTED};
        font-size:12px;
    ">
        Champion Model · Maximum Temperature Forecast
        · Updated {pd.Timestamp.now().strftime("%d %b %Y, %H:%M")}
    </div>
    """,
    unsafe_allow_html=True
)
