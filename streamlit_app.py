import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime

st.title("Control de Gastos")

# 1. Conexión limpia
conn = st.connection("gsheets", type=GSheetsConnection)

# 2. Leer datos (Si falla, crea una tabla vacía)
try:
    df_existente = conn.read(ttl=0)
except Exception:
    df_existente = pd.DataFrame(columns=['Fecha', 'Tipo', 'Categoría/Detalle', 'Monto', 'Moneda'])

# 3. Formulario simple
with st.form("mi_formulario"):
    fecha = st.date_input("Fecha", datetime.now())
    tipo = st.selectbox("Tipo", ["Gasto", "Ahorro", "Deuda"])
    detalle = st.text_input("Detalle")
    monto = st.number_input("Monto", min_value=0.0)
    moneda = st.selectbox("Moneda", ["ARS", "USD"])
    boton = st.form_submit_button("Guardar Registro")

    if boton:
        if detalle and monto > 0:
            nueva_fila = pd.DataFrame([{
                'Fecha': fecha.strftime('%d/%m/%Y'),
                'Tipo': tipo,
                'Categoría/Detalle': detalle,
                'Monto': monto,
                'Moneda': moneda
            }])
            
            # Combinar
            df_actualizado = pd.concat([df_existente, nueva_fila], ignore_index=True)
            
            # GUARDAR
            try:
                conn.update(data=df_actualizado)
                st.success("¡Guardado correctamente!")
                st.balloons()
            except Exception as e:
                st.error(f"Error al guardar: {e}")
        else:
            st.warning("Completa los datos")
