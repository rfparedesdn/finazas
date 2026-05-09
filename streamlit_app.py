import streamlit as st
import pandas as pd
from google.oauth2.service_account import Credentials
import gspread

# Configuración de credenciales directa
info = {
    "type": "service_account",
    "project_id": "capable-alcove-427523-u2",
    "private_key_id": "78e3a250f0c20b6a409b10076992ba6b86e4f5ed",
    "private_key": """-----BEGIN PRIVATE KEY-----
AQUÍ_PEGÁ_TU_LLAVE_MII_QUE_TENÉS_EN_EL_JSON
-----END PRIVATE KEY-----""",
    "client_email": "gastos-bot@capable-alcove-427523-u2.iam.gserviceaccount.com",
    "client_id": "111847215780906508573",
    "token_uri": "https://oauth2.google.com/token",
}

scope = ["https://www.googleapis.com/auth/spreadsheets"]

try:
    creds = Credentials.from_service_account_info(info, scopes=scope)
    client = gspread.authorize(creds)
    # Este es el ID de tu Google Sheet
    sheet = client.open_by_key("1TBW_be5E2fhIJePzxKD_iL79ltP6-APE4EJKTaWTAvs").sheet1
    st.success("¡Conexión establecida!")
except Exception as e:
    st.error(f"Error: {e}")

st.title("Prueba de Gastos")
detalle = st.text_input("Detalle")
monto = st.number_input("Monto", min_value=0)

if st.button("Guardar"):
    try:
        sheet.append_row([detalle, monto])
        st.success("¡Guardado en el Excel!")
        st.balloons()
    except Exception as e:
        st.error(f"No pude escribir en el Excel: {e}")
