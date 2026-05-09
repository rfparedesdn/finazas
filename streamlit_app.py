import streamlit as st
import pandas as pd
from google.oauth2.service_account import Credentials
import gspread

# --- CONFIGURACIÓN DE SEGURIDAD ---
# Pegá tu llave MII... dentro de las comillas triples, SIN los saltos de línea \n
raw_key = """-----BEGIN PRIVATE KEY-----
TU_LLAVE_MII_AQUÍ
-----END PRIVATE KEY-----"""

# Esto limpia cualquier carácter raro (como el 195) que se haya colado
clean_key = raw_key.replace('“', '"').replace('”', '"').replace('‘', "'").replace('’', "'")

info = {
    "type": "service_account",
    "project_id": "capable-alcove-427523-u2",
    "private_key_id": "78e3a250f0c20b6a409b10076992ba6b86e4f5ed",
    "private_key": clean_key,
    "client_email": "gastos-bot@capable-alcove-427523-u2.iam.gserviceaccount.com",
    "client_id": "111847215780906508573",
    "token_uri": "https://oauth2.google.com/token",
}

scope = ["https://www.googleapis.com/auth/spreadsheets"]

try:
    creds = Credentials.from_service_account_info(info, scopes=scope)
    client = gspread.authorize(creds)
    # ID de tu Excel
    sheet = client.open_by_key("1TBW_be5E2fhIJePzxKD_iL79ltP6-APE4EJKTaWTAvs").sheet1
    st.success("✅ ¡Conexión establecida con éxito!")
except Exception as e:
    st.error(f"❌ Error de llave: {e}")

st.title("💰 Control de Gastos")
detalle = st.text_input("Concepto")
monto = st.number_input("Importe", min_value=0)

if st.button("Guardar"):
    try:
        sheet.append_row([detalle, monto])
        st.success("¡Datos guardados!")
        st.balloons()
    except Exception as e:
        st.error(f"Error al escribir: {e}")
