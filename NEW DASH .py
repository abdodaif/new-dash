import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import networkx as nx
from datetime import datetime, timedelta
import random

# ────────────────────────────────
# Aman Payment Security – Live Dashboard 2025 (Dark)
# ────────────────────────────────

st.set_page_config(page_title="Aman Payment Security", layout="wide", page_icon="🛡️")

# ---- dark theme CSS + meta refresh 60s ----
st.markdown("""
<meta http-equiv="refresh" content="60">
<style>
    /* page background */
    .reportview-container, .main {
        background: linear-gradient(180deg,#0b1220 0%, #071026 100%);
        color: #e6eef8;
    }
    /* title */
    .big-title {font-size:44px !important; font-weight:800; color:#34d399; text-align:center; padding:6px 0 18px 0;}
    .kpi {font-size:36px; font-weight:700; color:#e6eef8;}
    .kpi-small {font-size:14px; color:#a6b4c6;}
    .card {background: linear-gradient(180deg, rgba(255,255,255,0.02), rgba(255,255,255,0.01)); padding:16px; border-radius:12px; box-shadow: 0 6px 24px rgba(2,6,23,0.6); border:1px solid rgba(255,255,255,0.03);}
    .small-muted {font-size:12px; color:#93a3b8;}
    .danger {color:#f87171; font-weight:700;}
    .safe {color:#34d399; font-weight:700;}
    .yellow {color:#fbbf24; font-weight:700;}
    table.dataframe {background:transparent;}
</style>
""", unsafe_allow_html=True)

# Header
st.markdown('<div style="display:flex;align-items:center;gap:16px;">'
            '<img src="https://via.placeholder.com/80x80.png?text=Aman" style="border-radius:12px;">'
            f'<div><p class="big-title">🛡️ Aman Payment Security – Live Fraud Shield (Dark)</p>'
            f'<p class="small-muted">Smart Fraud Detection & Analysis 2025 — Last updated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</p></div>'
            '</div>', unsafe_allow_html=True)

# -------------------------
# Data generator (rich)
# -------------------------
@st.cache_data(ttl=30)
def get_data(n=800):
    cities = ["القاهرة","الجيزة","الإسكندرية","الدقهلية","الشرقية","القليوبية","البحيرة","المنوفية","أسيوط","سوهاج"]
    merchants = ["Amazon","Noon","Talabat","Uber","Careem","Vodafone Cash","Fawry","InstaPay","Booking","Mobilis"]
    types = ["Card Testing","Account Takeover","Friendly Fraud","Bot Attack","Merchant Compromise"]
    rows = []
    now = datetime.now()
    for i in range(n):
        tx = {
            "transaction_id": f"TX{random.randint(1000000,9999999)}",
            "account_id": f"AC{random.randint(20000,99999)}",
            "merchant": random.choice(merchants),
            "city": random.choice(cities),
            "amount": random.randint(50, 15000),
            "risk_score": random.randint(500, 1000),
            "fraud_type": random.choices(types, weights=[0.25,0.15,0.2,0.25,0.15])[0],
            "status": random.choices(["BLOCKED","REVIEW","APPROVED"], weights=[0.18,0.22,0.60])[0],
            "timestamp": now - timedelta(minutes=random.randint(0, 1440))
        }
        rows.append(tx)
    df = pd.DataFrame(rows)
    return df

df = get_data(1200)

# -------------------------
# Top-level KPIs
# -------------------------
total = len(df)
blocked_count = df[df["status"] == "BLOCKED"].shape[0]
loss_saved = df[df["status"] == "BLOCKED"]["amount"].sum()
detection_rate = round((blocked_count / total) * 100, 2)
false_positive = round(random.uniform(0.2, 1.2), 2)  # simulated
precision = round(random.uniform(88.0, 98.0), 2)

k1, k2, k3, k4 = st.columns([2,2,2,2])
with k1:
    st.markdown('<div class="card"><div style="text-align:center;"><div class="kpi">{:,}</div><div class="kpi-small">إجمالي المعاملات</div></div></div>'.format(total), unsafe_allow_html=True)
with k2:
    st.markdown('<div class="card"><div style="text-align:center;"><div class="kpi danger">{:,}</div><div class="kpi-small">تم حظره (Blocked)</div></div></div>'.format(blocked_count), unsafe_allow_html=True)
with k3:
    st.markdown('<div class="card"><div style="text-align:center;"><div class="kpi safe">{:,} EGP</div><div class="kpi-small">تقديري: خسائر مُجنَبة</div></div></div>'.format(int(loss_saved)), unsafe_allow_html=True)
with k4:
    st.markdown('<div class="card"><div style="text-align:center;"><div class="kpi yellow">{:.2f}%</div><div class="kpi-small">Detection Rate</div></div></div>'.format(detection_rate), unsafe_allow_html=True)

st.markdown("---")

# -------------------------
# Layout: left (map + trend + network), right (top table + merchants + histogram)
# -------------------------
left, right = st.columns([2,1])

# LEFT
with left:
    # Map
    st.subheader("📍 توزيع عمليات الاحتيال — مصر (آخر 24 ساعة)")
    egypt_coords = {
        "القاهرة": [30.0444, 31.2357], "الجيزة": [30.0131, 31.2089], "الإسكندرية": [31.2001, 29.9187],
        "الدقهلية": [31.0467, 31.3785], "الشرقية": [30.5972, 31.5021], "القليوبية": [30.3292, 31.2089],
        "البحيرة": [31.0333, 30.4667], "المنوفية": [30.5972, 30.9876], "أسيوط": [27.1810, 31.1837],
        "سوهاج": [26.5591, 31.6957]
    }
    map_df = df.groupby("city").size().reset_index(name="count")
    map_df["lat"] = map_df["city"].map({k:v[0] for k,v in egypt_coords.items()})
    map_df["lon"] = map_df["city"].map({k:v[1] for k,v in egypt_coords.items()})
    fig_map = px.scatter_mapbox(map_df, lat="lat", lon="lon", size="count", color="count",
                                color_continuous_scale=px.colors.sequential.YlOrRd, size_max=40, zoom=5,
                                mapbox_style="carto-positron", hover_name="city", template="plotly_dark")
    fig_map.update_layout(margin=dict(l=0,r=0,t=0,b=0), mapbox=dict(center=dict(lat=30.5, lon=31.0)))
    st.plotly_chart(fig_map, use_container_width=True, theme="streamlit")

    st.markdown("### ⏱ Fraud Attempts — آخر 24 ساعة (ساعياً)")
    trend = df.copy()
    trend["hour"] = trend["timestamp"].dt.hour
    hourly = trend.groupby("hour").size().reset_index(name="count")
    fig_trend = px.line(hourly, x="hour", y="count", markers=True, title="Fraud Attempts per Hour (24h)", template="plotly_dark")
    fig_trend.update_layout(xaxis_title="Hour", yaxis_title="Count", margin=dict(t=30))
    st.plotly_chart(fig_trend, use_container_width=True)

    st.markdown("### 🌐 شبكات الاحتيال المكتشفة (Graph View)")
    # Build a simple graph: accounts <-> merchants via high risk transactions
    g_df = df[df["risk_score"] >= 800].sample(min(60, len(df[df["risk_score"] >= 800])))
    G = nx.Graph()
    # add nodes
    for _, row in g_df.iterrows():
        G.add_node(row["account_id"], label=row["account_id"], type="account")
        G.add_node(row["merchant"], label=row["merchant"], type="merchant")
        G.add_edge(row["account_id"], row["merchant"], weight= row["risk_score"]/1000)
    pos = nx.spring_layout(G, seed=42, k=0.8)
    edge_x = []
    edge_y = []
    for edge in G.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_x += [x0, x1, None]
        edge_y += [y0, y1, None]
    node_x = []
    node_y = []
    node_text = []
    node_color = []
    for node in G.nodes():
        x, y = pos[node]
        node_x.append(x)
        node_y.append(y)
        ntype = G.nodes[node].get("type", "")
        node_text.append(str(node))
        node_color.append("#34d399" if ntype=="account" else "#fb7185")
    edge_trace = go.Scatter(x=edge_x, y=edge_y, line=dict(width=1, color='#888'), hoverinfo='none', mode='lines')
    node_trace = go.Scatter(x=node_x, y=node_y, mode='markers+text',
                            marker=dict(size=14, color=node_color),
                            text=node_text, hoverinfo='text')
    Gfig = go.Figure(data=[edge_trace, node_trace])
    Gfig.update_layout(template="plotly_dark", showlegend=False, height=420, margin=dict(l=0,r=0,b=0,t=10))
    st.plotly_chart(Gfig, use_container_width=True)

# RIGHT
with right:
    st.subheader("🔥 أعلى 10 معاملات خطورة")
    # ensure the columns exist
    top10 = df.nlargest(10, "risk_score")[["transaction_id","amount","merchant","risk_score","city","status","timestamp"]]
    top10["amount"] = top10["amount"].astype(int)
    st.dataframe(top10.sort_values("risk_score", ascending=False).reset_index(drop=True), use_container_width=True, height=360)

    st.markdown("---")
    st.subheader("🏷️ أعلى التجّار استهدافاً (Top Merchants)")
    m = df.groupby("merchant").agg({"risk_score":"mean","transaction_id":"count","amount":"sum"}).reset_index()
    m = m.rename(columns={"transaction_id":"tx_count","amount":"total_amount"})
    m = m.sort_values("risk_score", ascending=False).head(8)
    fig_m = px.bar(m, x="merchant", y="tx_count", hover_data=["risk_score","total_amount"], template="plotly_dark")
    st.plotly_chart(fig_m, use_container_width=True)

    st.markdown("### 📊 توزيع درجات الخطر")
    fig_hist = px.histogram(df, x="risk_score", nbins=20, title="Risk Score Distribution", template="plotly_dark")
    st.plotly_chart(fig_hist, use_container_width=True)

# -------------------------
# Filters & Insights bottom
# -------------------------
st.markdown("---")
st.subheader("🔎 Filters & Insights")
cols = st.columns([1,1,1,1])
with cols[0]:
    city_filter = st.selectbox("Filter by City", options=["All"] + sorted(df["city"].unique().tolist()))
with cols[1]:
    merchant_filter = st.selectbox("Filter by Merchant", options=["All"] + sorted(df["merchant"].unique().tolist()))
with cols[2]:
    status_filter = st.selectbox("Filter by Status", options=["All","BLOCKED","REVIEW","APPROVED"])
with cols[3]:
    min_score = st.slider("Min risk score", 500, 1000, 700)

filtered = df.copy()
if city_filter != "All":
    filtered = filtered[filtered["city"] == city_filter]
if merchant_filter != "All":
    filtered = filtered[filtered["merchant"] == merchant_filter]
if status_filter != "All":
    filtered = filtered[filtered["status"] == status_filter]
filtered = filtered[filtered["risk_score"] >= min_score]

st.markdown(f"**Showing {len(filtered):,} transactions — last updated {datetime.now().strftime('%H:%M:%S')}**")
st.dataframe(filtered.sort_values("timestamp", ascending=False).head(200), use_container_width=True)

# Footer / branding
st.markdown("""
<div style="text-align:center;margin-top:24px;color:#7f8fa4;">
<strong style="color:#34d399;">Aman Payment Security – Smart Fraud Detection & Analysis 2025</strong>
<br>Enterprise Fraud Shield • Designed for Banks & Payment Providers
</div>
""", unsafe_allow_html=True)
