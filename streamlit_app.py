import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_gsheets import GSheetsConnection
from datetime import datetime

st.set_page_config(page_title="Finanzas Rafa", layout="wide")

st.title("📊 Mi Control de Finanzas (ARS/USD)")

# --- CONEXIÓN A GOOGLE SHEETS ---
# Usamos el link directo para que sea más fácil
url = st.secrets["connections"]["gsheets"]["spreadsheet"]
conn = st.connection("gsheets", type=GSheetsConnection)

# Leer datos existentes de la hoja
try:
    df_existente = conn.read(spreadsheet=url, ttl=0)
except Exception as e:
    st.error(f"Error al leer la hoja: {e}")
    df_existente = pd.DataFrame(columns=['Fecha', 'Tipo', 'Categoría/Detalle', 'Monto', 'Moneda'])

# Leer datos existentes de la hoja
try:
    df_existente = conn.read(ttl=0) # ttl=0 para que siempre lea lo último
except:
    # Si la hoja está vacía, crear estructura básica
    df_existente = pd.DataFrame(columns=['Fecha', 'Tipo', 'Categoría/Detalle', 'Monto', 'Moneda'])

# --- BARRA LATERAL ---
st.sidebar.header("📝 Nuevo Movimiento")

tipo_registro = st.sidebar.selectbox("¿Qué vas a registrar?", ["Ahorro", "Gasto", "Deuda"])
moneda = st.sidebar.radio("Moneda", ["ARS", "USD"], horizontal=True)

if tipo_registro == "Ahorro":
    detalle = st.sidebar.selectbox("Categoría", ["Efectivo", "Inversiones CDR", "DolarApp", "Otros"])
elif tipo_registro == "Gasto":
    detalle = st.sidebar.text_input("Concepto del gasto")
else:
    detalle = st.sidebar.text_input("¿A quién le debés?")

monto = st.sidebar.number_input(f"Monto en {moneda}", min_value=0.0, step=10.0)

if st.sidebar.button("💾 Guardar en Google Sheets"):
    nueva_fila = pd.DataFrame([{
        'Fecha': datetime.now().strftime("%d/%m/%Y %H:%M"),
        'Tipo': tipo_registro,
        'Categoría/Detalle': detalle,
        'Monto': monto,
        'Moneda': moneda
    }])
    
 # Combinar con datos viejos y guardar
    df_actualizado = pd.concat([df_existente, nueva_fila], ignore_index=True)
    url = st.secrets["connections"]["gsheets"]["spreadsheet"]
    conn.update(spreadsheet=url, data=df_actualizado)
    st.sidebar.success("¡Guardado correctamente!")

# --- CUERPO PRINCIPAL ---
tab1, tab2, tab3 = st.tabs(["💰 Ahorros", "📉 Gastos", "💸 Deudas"])

with tab1:
    df_ahorros = df_existente[df_existente['Tipo'] == 'Ahorro']
    col1, col2 = st.columns(2)
    
    with col1:
        total_ars = df_ahorros[df_ahorros['Moneda'] == 'ARS']['Monto'].sum()
        st.metric("Total Ahorros ARS", f"$ {total_ars:,.2f}")
    with col2:
        total_usd = df_ahorros[df_ahorros['Moneda'] == 'USD']['Monto'].sum()
        st.metric("Total Ahorros USD", f"u$s {total_usd:,.2f}")

    if not df_ahorros.empty:
        fig = px.pie(df_ahorros, values='Monto', names='Categoría/Detalle', title="Distribución", hole=0.4)
        st.plotly_chart(fig)
    st.dataframe(df_ahorros, use_container_width=True)

with tab2:
    df_gastos = df_existente[df_existente['Tipo'] == 'Gasto']
    st.subheader("Listado de Gastos Realizados")
    
    g_ars = df_gastos[df_gastos['Moneda'] == 'ARS']['Monto'].sum()
    g_usd = df_gastos[df_gastos['Moneda'] == 'USD']['Monto'].sum()
    
    st.write(f"**Total Gastado:** ARS $ {g_ars:,.2f} | USD u$s {g_usd:,.2f}")
    st.table(df_gastos[['Fecha', 'Categoría/Detalle', 'Monto', 'Moneda']])

with tab3:
    df_deudas = df_existente[df_existente['Tipo'] == 'Deuda']
    if not df_deudas.empty:
        st.warning("⚠️ Tenés deudas pendientes")
        st.dataframe(df_deudas, use_container_width=True)
    else:
        st.success("¡Sin deudas!")

# Mostrar toda la base de datos al final por seguridad
if st.checkbox("Ver todos los registros"):
    st.write(df_existente)
