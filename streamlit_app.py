import streamlit as st
import pandas as pd
from datetime import datetime

st.title("Control de Gastos - Rafael")

# Usamos el ID de tu hoja directamente
SHEET_ID = '1TBW_be5E2fhIJePzxKD_iL79ltP6-APE4EJKTaWTAvs'
# Formato para leer y escribir vía CSV (truco para saltar bloqueos)
SHEET_URL = f'https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv'

# Intentar leer datos
try:
    df_existente = pd.read_csv(SHEET_URL)
except:
    df_existente = pd.DataFrame(columns=['Fecha', 'Tipo', 'Detalle', 'Monto', 'Moneda'])

with st.form("registro_gastos"):
    fecha = st.date_input("Fecha", datetime.now())
    tipo = st.selectbox("Tipo", ["Gasto", "Ahorro", "Deuda"])
    detalle = st.text_input("Detalle")
    monto = st.number_input("Monto", min_value=0.0)
    moneda = st.selectbox("Moneda", ["ARS", "USD"])
    boton = st.form_submit_button("Guardar Registro")

    if boton:
        if detalle and monto > 0:
            st.success(f"Dato listo: {detalle} - {monto} {moneda}")
            st.info("Copiá esta línea y pegala en tu Excel manualmente por ahora para no perder el dato.")
            st.code(f"{fecha},{tipo},{detalle},{monto},{moneda}")
            
            # NOTA: Para escribir automático sin el archivo JSON que no tenemos, 
            # Google exige que uses Google Forms como intermediario. 
            st.warning("Rafael, para que el botón guarde SOLO, necesitás conectar un Google Form.")
        else:
            st.error("Faltan datos")
