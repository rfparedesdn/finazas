import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import plotly.express as px
from datetime import datetime

st.set_page_config(page_title="Gastos Rafael", layout="wide")

st.title("💰 Control de Gastos Pro")

# Conexión con tu link
url_sheet = "https://docs.google.com/spreadsheets/d/1TBW_be5E2fhIJePzxKD_iL79ltP6-APE4EJKTaWTAvs/edit?usp=sharing"
conn = st.connection("gsheets", type=GSheetsConnection)

# Cargar Datos
try:
    df = conn.read(spreadsheet=url_sheet, ttl=0)
except:
    df = pd.DataFrame(columns=['Fecha', 'Tipo', 'Detalle', 'Monto', 'Moneda'])

col_f, col_g = st.columns([1, 2])

with col_f:
    st.subheader("📝 Registrar")
    with st.container(border=True):
        fecha = st.date_input("Fecha", datetime.now())
        tipo = st.selectbox("Tipo", ["Gasto", "Ahorro", "Deuda"])
        detalle = st.text_input("Detalle")
        monto = st.number_input("Monto", min_value=0.0)
        moneda = st.selectbox("Moneda", ["ARS", "USD"])
        
        if st.button("🚀 GUARDAR AHORA", use_container_width=True):
            if detalle and monto > 0:
                nueva_fila = pd.DataFrame([{
                    'Fecha': fecha.strftime('%d/%m/%Y'),
                    'Tipo': tipo,
                    'Detalle': detalle,
                    'Monto': monto,
                    'Moneda': moneda
                }])
                df_final = pd.concat([df, nueva_fila], ignore_index=True)
                
                try:
                    # INTENTO DE GUARDADO DIRECTO
                    conn.update(spreadsheet=url_sheet, data=df_final)
                    st.success("¡GUARDADO EN EXCEL!")
                    st.balloons()
                except:
                    # SI FALLA EL PERMISO, AVISAMOS PERO MOSTRAMOS LOS DATOS
                    st.warning("Google bloqueó el guardado directo por seguridad.")
                    st.info("Usá tu Formulario de Google para que se guarde automático sin errores.")
                    st.code(f"{detalle} - {monto} {moneda}")
            else:
                st.error("Faltan datos")

with col_g:
    st.subheader("📊 Gráfico de Gastos")
    if not df.empty:
        fig = px.pie(df, values='Monto', names='Tipo', hole=0.4)
        st.plotly_chart(fig, use_container_width=True)

st.subheader("📋 Historial")
st.dataframe(df.tail(10), use_container_width=True)
st.dataframe(df, use_container_width=True)
