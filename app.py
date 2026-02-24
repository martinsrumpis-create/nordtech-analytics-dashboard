
import streamlit as st
import pandas as pd
import plotly.express as px

# Konfigurācija
st.set_page_config(page_title="NordTech Dashboard", layout="wide")
st.title("🛡️ NordTech Stratēģiskais Uzraudzības Panelis")

@st.cache_data
def load_data():
    # Svarīgi: fails bez mapes ceļa, jo tas būs tajā pašā mapē
    df = pd.read_csv('enriched_data.csv')
    df['Date'] = pd.to_datetime(df['Date'])
    return df

try:
    df = load_data()
    st.sidebar.header("🎯 Vadības Filtri")
    selected_cats = st.sidebar.multiselect("Kategorijas", options=df['Product_Category'].unique(), default=df['Product_Category'].unique())
    f_df = df[df['Product_Category'].isin(selected_cats)]

    k1, k2, k3 = st.columns(3)
    k1.metric("Faktiskie Ieņēmumi", f"${f_df['Final_Revenue'].sum():,.0f}")
    k2.metric("Atgriešanas Rate", f"{(len(f_df[f_df['Status'] == 'Processed']) / len(f_df) * 100):.1f}%")
    k3.metric("Klientu Signāli", len(f_df))

    st.plotly_chart(px.area(f_df.groupby('Date')['Final_Revenue'].sum().reset_index(), x='Date', y='Final_Revenue', title="Peļņas plūsma"), use_container_width=True)
    
    if 'Complaint_Category' in f_df.columns:
        st.plotly_chart(px.pie(f_df, names='Complaint_Category', hole=0.5, title="Sūdzību iemesli"), use_container_width=True)
except Exception as e:
    st.error(f"Kļūda: {e}")
