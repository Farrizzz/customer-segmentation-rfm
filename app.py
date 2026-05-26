"""
Project 2: Customer Segmentation Dashboard
Jalankan dengan: streamlit run app.py
"""

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# ── Konfigurasi halaman ──────────────────────────────────────
st.set_page_config(
    page_title="Customer Segmentation Dashboard",
    page_icon="🛍️",
    layout="wide",
    initial_sidebar_state="expanded"
)

SEG_COLORS = {
    'Champions'      : '#2A9D8F',
    'Loyal Customers': '#E9C46A',
    'At Risk'        : '#E76F51',
    'Lost Customers' : '#264653',
}
SEG_ORDER = ['Champions', 'Loyal Customers', 'At Risk', 'Lost Customers']

SEG_EMOJI = {
    'Champions'      : '🏆',
    'Loyal Customers': '💛',
    'At Risk'        : '⚠️',
    'Lost Customers' : '😴',
}

SEG_ACTION = {
    'Champions'      : 'Berikan reward eksklusif & loyalty program',
    'Loyal Customers': 'Tawarkan upsell & bundle produk premium',
    'At Risk'        : 'Kirim win-back email + diskon personal 15%',
    'Lost Customers' : 'Evaluasi cost, fokus ke segmen lain',
}

# ── Load data ────────────────────────────────────────────────
@st.cache_data
def load_data():
    try:
        df = pd.read_csv('rfm_clustered.csv')
        return df
    except FileNotFoundError:
        st.error("File 'rfm_clustered.csv' tidak ditemukan. Jalankan notebook 1 & 2 terlebih dahulu.")
        st.stop()

rfm = load_data()

# ── Sidebar ──────────────────────────────────────────────────
st.sidebar.image("https://img.icons8.com/fluency/96/shop.png", width=60)
st.sidebar.title("🛍️ Customer Segmentation")
st.sidebar.markdown("---")

selected_segments = st.sidebar.multiselect(
    "Filter Segmen",
    options=SEG_ORDER,
    default=SEG_ORDER
)

min_monetary, max_monetary = st.sidebar.slider(
    "Filter Monetary (£)",
    min_value=int(rfm['Monetary'].min()),
    max_value=int(rfm['Monetary'].quantile(0.99)),
    value=(int(rfm['Monetary'].min()), int(rfm['Monetary'].quantile(0.99)))
)

st.sidebar.markdown("---")
st.sidebar.caption("Project 2 — Portfolio Data Analyst")
st.sidebar.caption("Dataset: Online Retail II (UCI)")

# Filter data
filtered = rfm[
    (rfm['Segment'].isin(selected_segments)) &
    (rfm['Monetary'] >= min_monetary) &
    (rfm['Monetary'] <= max_monetary)
]

# ── Header ───────────────────────────────────────────────────
st.title("🛍️ Customer Segmentation Dashboard")
st.markdown("Analisis RFM + K-Means Clustering untuk segmentasi pelanggan retail")
st.markdown("---")

# ── KPI Cards ────────────────────────────────────────────────
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Total Pelanggan", f"{len(filtered):,}")
with col2:
    st.metric("Total Revenue", f"£{filtered['Monetary'].sum():,.0f}")
with col3:
    st.metric("Avg Revenue/Customer", f"£{filtered['Monetary'].mean():,.0f}")
with col4:
    champ_pct = len(filtered[filtered['Segment']=='Champions']) / max(len(filtered),1) * 100
    st.metric("Champions %", f"{champ_pct:.1f}%")

st.markdown("---")

# ── Row 1: Distribusi & Revenue ──────────────────────────────
col_left, col_right = st.columns(2)

with col_left:
    st.subheader("Distribusi Pelanggan per Segmen")
    seg_counts = filtered['Segment'].value_counts().reindex(SEG_ORDER).fillna(0)
    fig_pie = px.pie(
        values=seg_counts.values,
        names=seg_counts.index,
        color=seg_counts.index,
        color_discrete_map=SEG_COLORS,
        hole=0.4
    )
    fig_pie.update_traces(textposition='inside', textinfo='percent+label')
    fig_pie.update_layout(showlegend=False, margin=dict(t=10, b=10, l=10, r=10), height=320)
    st.plotly_chart(fig_pie, use_container_width=True)

with col_right:
    st.subheader("Revenue per Segmen")
    seg_rev = filtered.groupby('Segment')['Monetary'].sum().reindex(SEG_ORDER).fillna(0)
    fig_bar = px.bar(
        x=seg_rev.index,
        y=seg_rev.values,
        color=seg_rev.index,
        color_discrete_map=SEG_COLORS,
        labels={'x': 'Segmen', 'y': 'Total Revenue (£)'},
        text=[f'£{v:,.0f}' for v in seg_rev.values]
    )
    fig_bar.update_traces(textposition='outside')
    fig_bar.update_layout(showlegend=False, margin=dict(t=10, b=10, l=10, r=10), height=320)
    st.plotly_chart(fig_bar, use_container_width=True)

# ── Row 2: RFM Scatter & Snake Chart ─────────────────────────
col_left2, col_right2 = st.columns(2)

with col_left2:
    st.subheader("Scatter Plot: Frequency vs Monetary")
    fig_scatter = px.scatter(
        filtered.sample(min(2000, len(filtered))),
        x='Monetary', y='Frequency',
        color='Segment',
        color_discrete_map=SEG_COLORS,
        size='M_Score',
        hover_data=['Customer ID', 'Recency', 'R_Score', 'F_Score', 'M_Score'],
        opacity=0.6
    )
    fig_scatter.update_layout(margin=dict(t=10, b=10, l=10, r=10), height=350)
    st.plotly_chart(fig_scatter, use_container_width=True)

with col_right2:
    st.subheader("Profil RFM per Segmen (Snake Chart)")
    seg_avg = filtered.groupby('Segment')[['R_Score','F_Score','M_Score']].mean().reindex(SEG_ORDER)
    fig_snake = go.Figure()
    for seg in SEG_ORDER:
        if seg in seg_avg.index and seg in selected_segments:
            fig_snake.add_trace(go.Scatter(
                x=['Recency', 'Frequency', 'Monetary'],
                y=seg_avg.loc[seg].values,
                mode='lines+markers',
                name=seg,
                line=dict(color=SEG_COLORS[seg], width=3),
                marker=dict(size=10)
            ))
    fig_snake.update_layout(
        yaxis=dict(range=[0, 5.5], title='Skor (1–5)'),
        margin=dict(t=10, b=10, l=10, r=10),
        height=350,
        legend=dict(orientation='h', y=-0.2)
    )
    st.plotly_chart(fig_snake, use_container_width=True)

# ── Row 3: Rekomendasi per Segmen ────────────────────────────
st.markdown("---")
st.subheader("🎯 Rekomendasi Strategi per Segmen")

cols = st.columns(len(selected_segments)) if len(selected_segments) <= 4 else st.columns(4)
for i, seg in enumerate(selected_segments):
    s = filtered[filtered['Segment'] == seg]
    with cols[i % 4]:
        st.markdown(
            f"""
            <div style='background:{SEG_COLORS[seg]}20; border-left: 4px solid {SEG_COLORS[seg]};
                        border-radius:8px; padding:12px; margin-bottom:8px;'>
                <b style='font-size:15px;'>{SEG_EMOJI[seg]} {seg}</b><br>
                <small>{len(s):,} pelanggan</small><br><br>
                <b>Avg Revenue:</b> £{s['Monetary'].mean():,.0f}<br>
                <b>Avg Recency:</b> {s['Recency'].mean():.0f} hari<br>
                <b>Avg Freq:</b> {s['Frequency'].mean():.1f} order<br><br>
                <i style='font-size:12px; color:#555;'>📌 {SEG_ACTION[seg]}</i>
            </div>
            """,
            unsafe_allow_html=True
        )

# ── Row 4: Tabel Data ─────────────────────────────────────────
st.markdown("---")
st.subheader("📋 Data Pelanggan")
show_cols = ['Customer ID', 'Segment', 'Recency', 'Frequency', 'Monetary',
             'R_Score', 'F_Score', 'M_Score', 'RFM_Total']

seg_filter_table = st.selectbox("Tampilkan segmen:", ['Semua'] + SEG_ORDER)
table_df = filtered if seg_filter_table == 'Semua' else filtered[filtered['Segment'] == seg_filter_table]
table_df = table_df[show_cols].sort_values('Monetary', ascending=False).reset_index(drop=True)

st.dataframe(
    table_df.head(100),
    use_container_width=True,
    height=300
)
st.caption(f"Menampilkan {min(100, len(table_df)):,} dari {len(table_df):,} pelanggan")

# Download button
csv = table_df.to_csv(index=False).encode('utf-8')
st.download_button(
    label="⬇️ Download CSV",
    data=csv,
    file_name=f"customers_{seg_filter_table.lower().replace(' ','_')}.csv",
    mime='text/csv'
)
