import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# 1. KONFIGURĀCIJA - Šī rinda ir vissvarīgākā vizuālajam izskatam!
st.set_page_config(
    page_title="NordTech Executive Dashboard", 
    layout="wide", # Šis izletina saturu pa visu ekrānu
    page_icon="🛡️"
)

# 2. Vizuālais stils (CSS)
st.markdown("""
    <style>
    .main { background-color: #f8fafc; }
    .stMetric { 
        background-color: #ffffff; 
        padding: 20px; 
        border-radius: 12px; 
        box-shadow: 0 4px 6px rgba(0,0,0,0.05); 
        border: 1px solid #e2e8f0;
    }
    h2 { color: #1e3a8a; border-bottom: 2px solid #3b82f6; padding-bottom: 10px; margin-top: 30px; }
    </style>
    """, unsafe_allow_html=True)

@st.cache_data
def load_data():
    # Pārliecinies, ka fails GitHub ir ar šādu nosaukumu
    df = pd.read_csv('enriched_data.csv')
    df['Date'] = pd.to_datetime(df['Date'])
    return df

try:
    df = load_data()

    # --- SIDEBAR FILTRI ---
    st.sidebar.header("🎯 Vadības Kontrole")
    selected_cats = st.sidebar.multiselect(
        "Izvēlies kategorijas:", 
        options=df['Product_Category'].unique(), 
        default=df['Product_Category'].unique()
    )
    
    # Datuma filtrs
    min_date = df['Date'].min().date()
    max_date = df['Date'].max().date()
    date_range = st.sidebar.date_input("Periods:", [min_date, max_date])

    # Filtrēšana
    f_df = df[df['Product_Category'].isin(selected_cats)]
    if len(date_range) == 2:
        f_df = f_df[(f_df['Date'].dt.date >= date_range[0]) & (f_df['Date'].dt.date <= date_range[1])]

    # --- VIRSRAKSTS ---
    st.title("🛡️ NordTech: Stratēģiskais Uzraudzības Panelis")
    st.markdown("Integrēts skats uz uzņēmuma peļņas rādītājiem un klientu atsauksmēm vienuviet.")

    # --- 1. SADAĻA: KPI RĀDĪTĀJI (Vienā rindā) ---
    st.header("💰 1. Finanšu kopsavilkums")
    k1, k2, k3, k4 = st.columns(4)
    
    actual_rev = f_df['Final_Revenue'].sum()
    potential_rev = (f_df['Price'] * f_df['Quantity']).sum()
    leakage = potential_rev - actual_rev
    return_rate = (len(f_df[f_df['Status'] == 'Processed']) / len(f_df)) * 100 if len(f_df) > 0 else 0
    
    k1.metric("Faktiskie Ieņēmumi", f"${actual_rev:,.0f}")
    k2.metric("Ieņēmumu Noplūde", f"${leakage:,.0f}", 
              delta=f"-{(leakage/potential_rev*100 if potential_rev>0 else 0):.1f}%", 
              delta_color="inverse")
    k3.metric("Atgriešanas Rate", f"{return_rate:.1f}%")
    k4.metric("Klientu Signāli", len(f_df))

    # --- 2. SADAĻA: GRAFIKI (Divi blakus) ---
    st.header("📊 2. Kvalitātes un tendenču analīze")
    col_left, col_right = st.columns(2)
    
    with col_left:
        st.subheader("Sūdzību iemesli")
        fig_pie = px.pie(f_df, names='Complaint_Category', hole=0.5,
                        color_discrete_sequence=px.colors.sequential.RdBu)
        fig_pie.update_layout(margin=dict(t=30, b=0, l=0, r=0))
        st.plotly_chart(fig_pie, use_container_width=True)
        
    with col_right:
        st.subheader("Ieņēmumu dinamika")
        time_data = f_df.groupby('Date')['Final_Revenue'].sum().reset_index()
        fig_area = px.area(time_data, x='Date', y='Final_Revenue')
        fig_area.update_traces(line_color='#1e3a8a', fillcolor='rgba(30, 58, 138, 0.1)')
        fig_area.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig_area, use_container_width=True)

    # --- 3. SADAĻA: DATU TABULA ---
    st.header("📋 3. Operatīvie dati")
    st.dataframe(f_df.sort_values(by='Date', ascending=False).head(50), use_container_width=True)

except Exception as e:
    st.error(f"Kļūda ielādējot datus: {e}")
