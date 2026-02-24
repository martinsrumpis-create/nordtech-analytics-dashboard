import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Piespiežam mākonim izmantot pilnu ekrāna platumu
st.set_page_config(page_title="NordTech Executive Dashboard", layout="wide")

# 2. Datu ielāde
@st.cache_data
def load_data():
    df = pd.read_csv('enriched_data.csv')
    df['Date'] = pd.to_datetime(df['Date'])
    return df

df = load_data()

# 3. Virsraksts
st.title("🛡️ NordTech Stratēģiskais Uzraudzības Panelis")

# 4. KPI rinda (Viss vienā līnijā)
k1, k2, k3, k4 = st.columns(4)
actual_rev = df['Final_Revenue'].sum()
k1.metric("💰 Faktiskie Ieņēmumi", f"${actual_rev:,.0f}")
# ... pievieno pārējos k2, k3, k4 šeit ...

st.markdown("---") # Atdalošā līnija

# 5. Grafiku rinda (Divi blakus)
col_left, col_right = st.columns(2)

with col_left:
    st.subheader("Ieņēmumi pa kategorijām")
    fig_bar = px.bar(df.groupby('Product_Category')['Final_Revenue'].sum().reset_index(), 
                     x='Final_Revenue', y='Product_Category', orientation='h')
    st.plotly_chart(fig_bar, use_container_width=True)

with col_right:
    st.subheader("Sūdzību iemesli")
    fig_pie = px.pie(df, names='Complaint_Category', hole=0.5)
    st.plotly_chart(fig_pie, use_container_width=True)

# 6. Tabula apakšā
st.subheader("📋 Detalizēts reģistrs")
st.dataframe(df.head(20), use_container_width=True)
