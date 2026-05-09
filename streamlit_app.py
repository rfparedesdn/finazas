import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

st.set_page_config(page_title="Gastos de Rafael", layout="wide")

st.title("📊 Control de Gastos Personal")

# --- CONEXIÓN ---
SHEET_URL = "https://docs.google.com/spreadsheets/d/1TBW_be5E2fhIJePzxKD_iL79ltP6-APE4EJKTaWTAvs/gviz/tq?tqx=out:csv"

@st.cache_data(ttl=60)
def cargar_datos():
    try:
        return pd.read_csv(SHEET_URL)
    except:
        return pd.DataFrame(columns=['Fecha', 'Tipo', 'Detalle', 'Monto', 'Moneda'])

df = cargar_datos()

# --- TABLERO DE RESUMEN (Métricas con estilo) ---
col1, col2, col3 = st.columns(3)
if not df.empty:
    total_ars = df[df['Moneda'] == 'ARS']['Monto'].sum()
    total_usd = df[df['Moneda'] == 'USD']['Monto'].sum()
    col1.metric("Total Gastado (ARS)", f"${total_ars:,.0f}")
    col2.metric("Total Gastado (USD)", f"u$d {total_usd:,.0f}")
    col3.metric("Registros", len(df))

# --- GRÁFICOS (Para que no sea cuadrado) ---
st.markdown("---")
col_izq, col_der = st.columns(2)

with col_izq:
    if not df.empty:
        st.subheader("Distribución por Tipo")
        fig_pie = px.pie(df, values='Monto', names='Tipo', hole=0.4, 
                         color_discrete_sequence=px.colors.qualitative.Pastel)
        st.plotly_chart(fig_pie, use_container_width=True)

with col_der:
    st.subheader("Nuevo Registro")
    with st.container(border=True): # Esto le da un borde redondeado al formulario
        fecha = st.date_input("Fecha", datetime.now())
        tipo = st.selectbox("Categoría", ["Gasto", "Ahorro", "Deuda"])
        detalle = st.text_input("¿En qué gastaste?")
        monto = st.number_input("Monto", min_value=0.0)
        moneda = st.selectbox("Moneda", ["ARS", "USD"])
        
        btn = st.button("🚀 Guardar en mi Excel")
        
        if btn:
            if detalle and monto > 0:
                st.success(f"Listo Rafael. Copiá esto al Excel: {detalle} | {monto}")
                st.code(f"{fecha},{tipo},{detalle},{monto},{moneda}")
                st.balloons()
            else:
                st.error("Faltan datos")

# --- TABLA VISUAL ---
st.subheader("Últimos Movimientos")
st.dataframe(df.tail(10), use_container_width=True)
