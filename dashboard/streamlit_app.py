import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

st.set_page_config(page_title="Data Lifecycle Smart Farming Dashboard", layout="wide")

st.markdown("""
    <style>
    html, body, [class*="css"]  { font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; }
    
    .stApp { background-color: #F8FAF8; }
    
    /* CSS untuk menengahkan judul utama */
    .main-title { color: #1B5E20; font-weight: 800; letter-spacing: -1px; text-align: center; font-size: 40px; margin-bottom: 5px; }
    .sub-title { text-align: center; color: #555; margin-bottom: 30px; font-size: 16px; }
    
    h1, h2, h3 { color: #1B5E20 !important; font-weight: 800; letter-spacing: -1px; }
    
    div[data-testid="stVerticalBlockBorderWrapper"] {
        background-color: #FFFFFF !important;
        border-radius: 15px !important;
        border: 1px solid #E8F5E9 !important;
        box-shadow: 0 8px 25px rgba(0,0,0,0.15) !important; 
        padding: 15px !important;
        margin-bottom: 25px !important;
    }
    
    .js-plotly-plot .plotly .main-svg { background: transparent !important; }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">🌿 Smart Farming Analytics Dashboard 🌿</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Monitor data sensor, kesehatan tanaman, dan tren secara modern, akurat, dan interaktif.</div>', unsafe_allow_html=True)

@st.cache_data
def load_and_clean_data():
    df = pd.read_csv('data/raw/Smart_Farming_Crop_Yield_2024.csv')
    date_cols = ['timestamp', 'sowing_date', 'harvest_date']
    for col in date_cols:
        df[col] = pd.to_datetime(df[col], errors='coerce') 
    
    df = df.drop_duplicates().reset_index(drop=True)
    focus_cols = ['soil_moisture_%', 'temperature_C', 'humidity_%', 'soil_pH', 'yield_kg_per_hectare']
    
    for col in focus_cols:
        if col in df.columns:
            df[col] = df[col].fillna(df[col].median())
            Q1 = df[col].quantile(0.25)
            Q3 = df[col].quantile(0.75)
            IQR = Q3 - Q1
            df[col] = df[col].clip(lower=Q1 - 1.5 * IQR, upper=Q3 + 1.5 * IQR)
        
    return df

try:
    df = load_and_clean_data()
except FileNotFoundError:
    df = pd.DataFrame()

if df.empty:
    dates = pd.date_range(start='2024-01-01', periods=100, freq='D')
    df_ts = pd.DataFrame({'timestamp': dates, 'temperature_C': 25, 'soil_moisture_%': 45, 'humidity_%': 60, 'soil_pH': 6.5, 'NDVI_index': 0.75, 'yield_kg_per_hectare': 5000, 'crop_type': 'Wheat'}).set_index('timestamp')
else:
    df_ts = df.set_index('timestamp').sort_index()

min_date = df_ts.index.min().date()
max_date = df_ts.index.max().date()

col_filter1, col_filter2, col_filter3 = st.columns([1.2, 1, 1])

with col_filter1:
    with st.container(border=True):
        st.markdown('<div style="font-weight: 700; color: #1B5E20;">Rentang Waktu:</div>', unsafe_allow_html=True)
        selected_dates = st.slider(
            "label_hidden",
            min_value=min_date,
            max_value=max_date,
            value=(min_date, max_date),
            format="DD MMM YYYY",
            label_visibility="collapsed"
        )

with col_filter2:
    with st.container(border=True):
        st.markdown('<div style="font-weight: 700; color: #1B5E20;">Resolusi:</div>', unsafe_allow_html=True)
        time_resolution = st.radio(
            "radio_label_hidden",
            options=["Harian", "Mingguan", "Bulanan"],
            horizontal=True,
            label_visibility="collapsed"
        )

with col_filter3:
    with st.container(border=True):
        st.markdown('<div style="font-weight: 700; color: #1B5E20;">Jenis Tanaman:</div>', unsafe_allow_html=True)
        crop_options = ["Semua Tanaman"] + list(df_ts['crop_type'].unique()) if 'crop_type' in df_ts.columns else ["Semua Tanaman"]
        selected_crop = st.selectbox(
            "crop_label_hidden",
            options=crop_options,
            label_visibility="collapsed"
        )

st.divider()

if selected_crop != "Semua Tanaman":
    df_ts_filtered_crop = df_ts[df_ts['crop_type'] == selected_crop]
else:
    df_ts_filtered_crop = df_ts.copy()

mask = (df_ts_filtered_crop.index.date >= selected_dates[0]) & (df_ts_filtered_crop.index.date <= selected_dates[1])
df_filtered = df_ts_filtered_crop.loc[mask]

if not df_filtered.empty:
    numeric_cols = df_filtered.select_dtypes(include='number').columns
    if time_resolution == "Harian":
        df_resampled = df_filtered[numeric_cols].resample('D').mean().dropna()
    elif time_resolution == "Mingguan":
        df_resampled = df_filtered[numeric_cols].resample('W').mean().dropna()
    else:
        df_resampled = df_filtered[numeric_cols].resample('ME').mean().dropna()
else:
    df_resampled = pd.DataFrame()

if not df_resampled.empty:
    current_moisture = df_resampled['soil_moisture_%'].tail(5).mean()
    if 'NDVI_index' in df_resampled.columns:
        current_ndvi = df_resampled['NDVI_index'].tail(5).mean()
    else:
        current_ndvi = 0.75
else:
    current_moisture = 0
    current_ndvi = 0

# Threshold & Alert System

if len(df_resampled) >= 2:
    prev_moisture = df_resampled['soil_moisture_%'].iloc[-2]
    moisture_delta = current_moisture - prev_moisture
    
    prev_ndvi = df_resampled['NDVI_index'].iloc[-2] if 'NDVI_index' in df_resampled.columns else current_ndvi
    ndvi_delta = current_ndvi - prev_ndvi
else:
    moisture_delta = 0
    ndvi_delta = 0

m_symbol = "↑" if moisture_delta >= 0 else "↓"
n_symbol = "↑" if ndvi_delta >= 0 else "↓"

col_alert1, col_alert2 = st.columns(2)

with col_alert1:
    bg_m = "#FF5252" if current_moisture < 20 else "#2E7D32" 
    status_text = "Irigasi diperlukan" if current_moisture < 20 else "Kondisi optimal"
    
    st.markdown(f"""
        <div style="background-color: {bg_m}; border-radius: 15px; padding: 25px; text-align: center; color: white; box-shadow: 0 4px 12px rgba(0,0,0,0.1);">
            <div style="font-size: 28px; font-weight: 700; opacity: 1;">Kelembapan Tanah Rata-rata</div>
            <div style="font-size: 50px; font-weight: 800; margin: 10px 0;">
                {current_moisture:.1f}% 
                <span style="font-size: 22px; opacity: 0.8; font-weight: 400;">({m_symbol} {abs(moisture_delta):.1f}%)</span>
            </div>
            <div style="font-size: 20px; font-weight: 600;">{status_text}</div>
        </div>
    """, unsafe_allow_html=True)

with col_alert2:
    bg_n = "#FF5252" if current_ndvi < 0.3 else "#2E7D32"
    status_text2 = "Kesehatan buruk" if current_ndvi < 0.3 else "Tanaman sehat"
    
    st.markdown(f"""
        <div style="background-color: {bg_n}; border-radius: 15px; padding: 25px; text-align: center; color: white; box-shadow: 0 4px 12px rgba(0,0,0,0.1);">
            <div style="font-size: 28px; font-weight: 700; opacity: 1;">Kesehatan Tanaman (NDVI)</div>
            <div style="font-size: 50px; font-weight: 800; margin: 10px 0;">
                {current_ndvi:.2f}
                <span style="font-size: 22px; opacity: 0.8; font-weight: 400;">({n_symbol} {abs(ndvi_delta):.2f})</span>
            </div>
            <div style="font-size: 20px; font-weight: 600;">{status_text2}</div>
        </div>
    """, unsafe_allow_html=True)

st.divider()

# Gauge Meter

st.markdown("### Soil Moisture Status Gauge")

fig_gauge = go.Figure(go.Indicator(
    mode = "gauge+number",
    value = current_moisture,
    domain = {'x': [0, 1], 'y': [0, 1]},
    title = {'text': "Moisture (%)", 'font': {'size': 18, 'color': '#7F8C8D'}},
    number = {
        'font': {
            'size': 70, 
            'color': '#1B5E20',
            'weight': 'bold',
        }
    },
    gauge = {
        'axis': {'range': [0, 100], 'tickwidth': 1, 'tickcolor': "#7F8C8D", 'tickfont': {'size': 10}},
        'bar': {'color': "#1B5E20"},
        'bgcolor': "rgba(0,0,0,0)",
        'borderwidth': 0,
        'steps': [
            {'range': [0, 20], 'color': '#FFCDD2'},
            {'range': [20, 60], 'color': '#C8E6C9'},
            {'range': [60, 100], 'color': '#BBDEFB'}
        ],
        'threshold': {'line': {'color': "#D32F2F", 'width': 4}, 'thickness': 0.75, 'value': 20}
    }
))

fig_gauge.update_layout(height=260, margin=dict(l=50, r=50, t=10, b=0), paper_bgcolor="rgba(0,0,0,0)")
st.plotly_chart(fig_gauge, use_container_width=True)

st.markdown("""
<div style="text-align: center; font-size: 14px; color: #7F8C8D; margin-top: -15px;">
    <b>Keterangan Zona:</b><br>
    <span style="color: #FF5252;">■ 0-20% (Kritis/Kering)</span> &nbsp;|&nbsp; 
    <span style="color: #4CAF50;">■ 20-60% (Optimal)</span> &nbsp;|&nbsp; 
    <span style="color: #64B5F6;">■ 60-100% (Terlalu Basah)</span>
</div>
""", unsafe_allow_html=True)

st.divider()

# Line Chart

st.markdown("### Sensor Trend Analysis")

if not df_resampled.empty:
    trend_data = df_resampled.reset_index()

    fig_temp = px.line(trend_data, x='timestamp', y='temperature_C', labels={'temperature_C': '°C', 'timestamp': 'Date'})
    fig_temp.update_traces(line_color='#E74C3C', line_width=3)

    fig_moist = px.line(trend_data, x='timestamp', y='soil_moisture_%', labels={'soil_moisture_%': '%', 'timestamp': 'Date'})
    fig_moist.update_traces(line_color='#2E7D32', line_width=3)

    fig_hum = px.line(trend_data, x='timestamp', y='humidity_%', labels={'humidity_%': '%', 'timestamp': 'Date'})
    fig_hum.update_traces(line_color='#3498DB', line_width=3)

    fig_ph = px.line(trend_data, x='timestamp', y='soil_pH', labels={'soil_pH': 'pH', 'timestamp': 'Date'})
    fig_ph.update_traces(line_color='#9b59b6', line_width=3)

    def beautify_line_chart(fig, title_text):
        fig.update_layout(
            title = {'text': title_text, 'font': {'size': 18, 'weight': 'bold', 'color': '#1B5E20'}, 'x': 0.01},
            height = 280, margin = dict(l=30, r=30, t=50, b=20),
            plot_bgcolor='rgba(0,0,0,0)', 
            paper_bgcolor='rgba(0,0,0,0)', 
            xaxis = (dict(showgrid=False, zeroline=False)),
            yaxis = (dict(showgrid=True, gridcolor='#F1F1F1', zeroline=False))
        )

    beautify_line_chart(fig_temp, "Temperature (°C)")
    beautify_line_chart(fig_moist, "Soil Moisture (%)")
    beautify_line_chart(fig_hum, "Humidity (%)")
    beautify_line_chart(fig_ph, "Soil pH")

    with st.container(border=True):
        st.plotly_chart(fig_temp, use_container_width=True)

    with st.container(border=True):
        st.plotly_chart(fig_moist, use_container_width=True)

    with st.container(border=True):
        st.plotly_chart(fig_hum, use_container_width=True)

    with st.container(border=True):
        st.plotly_chart(fig_ph, use_container_width=True)
else:
    st.warning("Tidak ada data pada rentang waktu ini.")

st.divider()

# Colerration Heat Map

st.markdown("### Correlation Matrix (Heatmap)")

if not df_resampled.empty:
    focus_cols = ['soil_moisture_%', 'temperature_C', 'humidity_%', 'soil_pH', 'yield_kg_per_hectare']
    available_cols = [col for col in focus_cols if col in df_resampled.columns]
    
    corr = df_resampled[available_cols].corr()

    fig_heatmap = px.imshow(corr, text_auto=".2f", aspect="auto", color_continuous_scale="Greens", zmin=-1, zmax=1, labels=dict(x="Metric", y="Metric", color="Correlation"))

    fig_heatmap.update_layout(
        height=450, margin=dict(l=30, r=30, t=20, b=20),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)', 
        coloraxis_showscale=True,
        xaxis_tickfont={'size': 11},
        yaxis_tickfont={'size': 11}
    )

    with st.container(border=True):
        st.plotly_chart(fig_heatmap, use_container_width=True)
        st.markdown("""
            <div style="text-align: center;">
                <small>Keterangan: Semakin hijau gelap kotak, semakin kuat korelasi positif antar variabel sensor.</small>
            </div>
            """, unsafe_allow_html=True)
else:
    st.warning("Tidak ada data untuk membuat heatmap.")

st.markdown("""
    <div style="text-align: center; color: #7F8C8D; padding: 10px; font-size: 14px;">
        <hr style="solid #E8F5E9; margin-bottom: 20px;">23082010151 Savira Narita Rachman<br>
        <span style="font-size: 12px; opacity: 0.8;">Smart Farming Analytics Dashboard</span>
    </div>
""", unsafe_allow_html=True)