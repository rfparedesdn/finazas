import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Mi Control de Finanzas", layout="wide")

st.title("📊 Mi Control de Finanzas Personalizado")

# Inicializar estados si no existen
if 'ahorros' not in st.session_state:
    st.session_state.ahorros = pd.DataFrame(columns=['Categoría', 'Monto'])
if 'gastos' not in st.session_state:
    st.session_state.gastos = pd.DataFrame(columns=['Concepto', 'Monto'])
if 'deudas' not in st.session_state:
    st.session_state.deudas = pd.DataFrame(columns=['A quien', 'Monto'])

# --- BARRA LATERAL PARA ENTRADA DE DATOS ---
st.sidebar.header("📝 Registro de Movimientos")

tipo_registro = st.sidebar.selectbox("¿Qué vas a registrar?", ["Ahorro", "Gasto", "Deuda"])

if tipo_registro == "Ahorro":
    cat_ahorro = st.sidebar.selectbox("Categoría", ["Efectivo", "Inversiones CDR", "DolarApp", "Otros"])
    monto_ahorro = st.sidebar.number_input("Monto del ahorro", min_value=0.0, step=100.0)
    if st.sidebar.button("Agregar Ahorro"):
        nuevo_ahorro = pd.DataFrame({'Categoría': [cat_ahorro], 'Monto': [monto_ahorro]})
        st.session_state.ahorros = pd.concat([st.session_state.ahorros, nuevo_ahorro], ignore_index=True)
        st.success("Ahorro guardado")

elif tipo_registro == "Gasto":
    concepto_gasto = st.sidebar.text_input("Concepto del gasto")
    monto_gasto = st.sidebar.number_input("Monto del gasto", min_value=0.0, step=50.0)
    if st.sidebar.button("Agregar Gasto"):
        nuevo_gasto = pd.DataFrame({'Concepto': [concepto_gasto], 'Monto': [monto_gasto]})
        st.session_state.gastos = pd.concat([st.session_state.gastos, nuevo_gasto], ignore_index=True)
        st.warning("Gasto registrado")

else:  # Deudas
    entidad_deuda = st.sidebar.text_input("¿A quién le debés?")
    monto_deuda = st.sidebar.number_input("Monto de la deuda", min_value=0.0, step=100.0)
    if st.sidebar.button("Agregar Deuda"):
        nueva_deuda = pd.DataFrame({'A quien': [entidad_deuda], 'Monto': [monto_deuda]})
        st.session_state.deudas = pd.concat([st.session_state.deudas, nueva_deuda], ignore_index=True)
        st.error("Deuda anotada")

# --- CUERPO PRINCIPAL CON PESTAÑAS ---
tab1, tab2, tab3 = st.tabs(["💰 Resumen de Ahorros", "📉 Gastos", "💸 Deudas Pendientes"])

with tab1:
    st.subheader("Distribución de mis Ahorros")
    if not st.session_state.ahorros.empty:
        fig_ahorros = px.pie(st.session_state.ahorros, values='Monto', names='Categoría', hole=0.4)
        st.plotly_chart(fig_ahorros)
        st.write(st.session_state.ahorros)
    else:
        st.info("Aún no hay ahorros registrados.")

with tab2:
    st.subheader("Listado de Gastos")
    if not st.session_state.gastos.empty:
        st.table(st.session_state.gastos)
        total_gastos = st.session_state.gastos['Monto'].sum()
        st.metric("Total Gastado", f"$ {total_gastos}")
    else:
        st.info("No hay gastos anotados.")

with tab3:
    st.subheader("Control de Deudas")
    if not st.session_state.deudas.empty:
        st.dataframe(st.session_state.deudas)
        total_deudas = st.session_state.deudas['Monto'].sum()
        st.subheader(f"Total a pagar: $ {total_deudas}")
    else:
        st.success("¡Felicidades! No tenés deudas registradas.")