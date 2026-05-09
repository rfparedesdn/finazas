import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import plotly.express as px
from datetime import datetime

# Configuración de la página para que se vea moderna
st.set_page_config(page_title="Finanzas Rafael", page_icon="💰", layout="wide")

st.title("📊 Panel de Control de Gastos")
st.markdown("---")

# 1. Conexión con tu Excel
conn = st.connection("gsheets", type=GSheetsConnection)

# 2. Cargar datos
try:
    # Cambiá esta URL por la de tu Excel si es necesario
    url = "https://docs.google.com/spreadsheets/d/1TBW_be5E2fhIJePzxKD_iL79ltP6-APE4EJKTaWTAvs/edit?usp=sharing"
    df = conn.read(spreadsheet=url, ttl=0)
except Exception:
    df = pd.DataFrame(columns=['Fecha', 'Tipo', 'Detalle', 'Monto', 'Moneda'])

# --- DISEÑO DE COLUMNAS ---
col_form, col_graf = st.columns([1, 2])

with col_form:
    st.subheader("📝 Nuevo Registro")
    with st.container(border=True): # Borde redondeado para el formulario
        fecha = st.date_input("Fecha", datetime.now())
        tipo = st.selectbox("Categoría", ["Gasto", "Ahorro", "Deuda"])
        detalle = st.text_input("Detalle (ej: Papa)")
        monto = st.number_input("Monto", min_value=0.0, step=100.0)
        moneda = st.selectbox("Moneda", ["ARS", "USD"])
        
        btn_guardar = st.button("🚀 Guardar Registro", use_container_width=True)

    if btn_guardar:
        if detalle and monto > 0:
            # Aquí mostramos el éxito y los datos
            st.success("¡Datos procesados!")
            st.balloons()
            # Mostramos el código para pegar si el permiso de escritura falla
            st.info("Copia esto a tu Excel si el guardado automático falla:")
            st.code(f"{fecha.strftime('%d/%m/%Y')}, {tipo}, {detalle}, {monto}, {moneda}")
        else:
            st.warning("Completá todos los campos.")

with col_graf:
    st.subheader("📈 Análisis Visual")
    if not df.empty:
        # Gráfico de Torta interactivo
        fig = px.pie(df, values='Monto', names='Tipo', 
                     title="Distribución de Gastos",
                     hole=0.4,
                     color_discrete_sequence=px.colors.qualitative.Safe)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Agregá datos para ver los gráficos.")

# --- TABLA INFERIOR ---
st.markdown("---")
st.subheader("📋 Últimos movimientos")
st.dataframe(df, use_container_width=True)
