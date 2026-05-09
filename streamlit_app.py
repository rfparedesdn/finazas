import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import plotly.express as px
from datetime import datetime

st.set_page_config(page_title="Gastos Rafael", layout="wide")

st.title("💰 Mi Control de Finanzas")

# 1. INTENTO DE CONEXIÓN
try:
    conn = st.connection("gsheets", type=GSheetsConnection)
    
    # URL de tu Excel
    URL_EXCEL = "https://docs.google.com/spreadsheets/d/1TBW_be5E2fhIJePzxKD_iL79ltP6-APE4EJKTaWTAvs/edit?usp=sharing"

    # Intentar leer
    df = conn.read(spreadsheet=URL_EXCEL, ttl=0)
    df = df.dropna(how='all')
    st.success("✅ ¡Conexión exitosa con el Excel!")

except Exception as e:
    st.error("❌ Error de Conexión")
    with st.expander("Ver detalle técnico del error"):
        st.write(e)
    
    st.info("💡 Si ya compartiste el archivo, revisá que en 'Secrets' de Streamlit hayas pegado la llave JSON correctamente.")
    df = pd.DataFrame(columns=['Fecha', 'Tipo', 'Detalle', 'Monto', 'Moneda'])

# --- RESTO DE LA INTERFAZ ---
col_form, col_graf = st.columns([1, 2])

with col_form:
    st.subheader("📝 Nuevo Registro")
    with st.container(border=True):
        fecha = st.date_input("Fecha", datetime.now())
        tipo = st.selectbox("Categoría", ["Gasto", "Ahorro", "Deuda", "Inversión"])
        detalle = st.text_input("¿En qué se usó?")
        monto = st.number_input("Monto", min_value=0.0, step=100.0)
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
                
                df_actualizado = pd.concat([df, nueva_fila], ignore_index=True)
                
                try:
                    conn.update(spreadsheet=URL_EXCEL, data=df_actualizado)
                    st.success("¡Guardado correctamente!")
                    st.balloons()
                    st.rerun()
                except Exception as ex:
                    st.error(f"No se pudo guardar: {ex}")
            else:
                st.warning("Completa los datos.")

with col_graf:
    st.subheader("📊 Resumen")
    if not df.empty:
        fig = px.pie(df, values='Monto', names='Tipo', hole=0.4)
        st.plotly_chart(fig, use_container_width=True)

st.subheader("📋 Historial")
st.dataframe(df.iloc[::-1], use_container_width=True, hide_index=True)
