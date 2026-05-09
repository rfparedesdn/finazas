import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import plotly.express as px
from datetime import datetime

# Configuración de la página
st.set_page_config(page_title="Gastos Rafael", layout="wide")

st.title("💰 Mi Control de Finanzas")

# 1. CONEXIÓN DIRECTA CON LA LLAVE JSON
# Usa el nombre que pusiste en los Secrets: [connections.gsheets]
conn = st.connection("gsheets", type=GSheetsConnection)

# URL de tu Excel (aseguráte que sea esta o cámbiala por la tuya)
URL_EXCEL = "https://docs.google.com/spreadsheets/d/1TBW_be5E2fhIJePzxKD_iL79ltP6-APE4EJKTaWTAvs/edit?usp=sharing"

# 2. LEER DATOS ACTUALES
try:
    # ttl=0 para que siempre traiga lo último y no use memoria vieja
    df = conn.read(spreadsheet=URL_EXCEL, ttl=0)
    
    # Limpieza: Si el Excel tiene filas vacías, las quitamos
    df = df.dropna(how='all')
except Exception as e:
    st.error("No se pudo conectar con el Excel. Revisá si compartiste el archivo con el correo del bot.")
    df = pd.DataFrame(columns=['Fecha', 'Tipo', 'Detalle', 'Monto', 'Moneda'])

# 3. INTERFAZ DE USUARIO (Dos columnas)
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
                # Crear la nueva fila
                nueva_fila = pd.DataFrame([{
                    'Fecha': fecha.strftime('%d/%m/%Y'),
                    'Tipo': tipo,
                    'Detalle': detalle,
                    'Monto': monto,
                    'Moneda': moneda
                }])
                
                # Combinar con los datos existentes
                df_actualizado = pd.concat([df, nueva_fila], ignore_index=True)
                
                # GUARDAR DIRECTO EN GOOGLE SHEETS
                try:
                    conn.update(spreadsheet=URL_EXCEL, data=df_actualizado)
                    st.success("¡Guardado correctamente!")
                    st.balloons()
                    st.rerun() # Esto refresca la app para ver el cambio
                except Exception as e:
                    st.error(f"Error al guardar: {e}")
            else:
                st.warning("Por favor, completa el detalle y el monto.")

with col_graf:
    st.subheader("📊 Resumen de Gastos")
    if not df.empty:
        # Gráfico circular
        fig = px.pie(df, values='Monto', names='Tipo', hole=0.4, 
                     color_discrete_sequence=px.colors.qualitative.Pastel)
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Aún no hay datos para mostrar gráficos.")

# 4. HISTORIAL (Limpio, sin repetir encabezados)
st.subheader("📋 Historial de Movimientos")
if not df.empty:
    # Mostramos los últimos 15 registros arriba
    st.dataframe(df.iloc[::-1], use_container_width=True, hide_index=True)
else:
    st.write("El historial está vacío.")
