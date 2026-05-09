import streamlit as st
import pandas as pd
from google.oauth2.service_account import Credentials
import gspread
import re

# --- ESTA ES LA FUNCIÓN DE LIMPIEZA TOTAL ---
def clean_pem_key(key):
    # Quitamos espacios locos, comillas curvas y caracteres raros
    key = key.replace('“', '"').replace('”', '"').replace('‘', "'").replace('’', "'")
    # Si la llave tiene los \n escritos, los convertimos en saltos de línea reales
    if "\\n" in key:
        key = key.replace("\\n", "\n")
    return key.strip()

# --- PEGA TU LLAVE ACÁ ADENTRO ---
# Asegurate de que empiece con -----BEGIN y termine con -----END
raw_key = """-----BEGIN PRIVATE KEY-----
TU_LLAVE_MII_AQUÍ_SIN_MIEDO
-----END PRIVATE KEY-----"""

info = {
    "type": "service_account",
    "project_id": "capable-alcove-427523-u2",
    "private_key_id": "78e3a250f0c20b6a409b10076992ba6b86e4f5ed",
    "private_key": clean_pem_key(raw_key),
    "client_email": "gastos-bot@capable-alcove-427523-u2.iam.gserviceaccount.com",
    "client_id": "111847215780906508573",
    "token_uri": "https://oauth2.google.com/token",
}

scope = ["https://www.googleapis.com/auth/spreadsheets"]

try:
    creds = Credentials.from_service_account_info(info, scopes=scope)
    client = gspread.authorize(creds)
    # Tu ID de Excel
    sheet = client.open_by_key("1TBW_be5E2fhIJePzxKD_iL79ltP6-APE4EJKTaWTAvs").sheet1
    st.success("✅ ¡CONECTADO POR FIN!")
except Exception as e:
    st.error(f"❌ Error de llave: {e}")
    st.info("Revisá que no haya guiones bajos (_) perdidos al principio de la llave.")

st.title("💰 Control de Gastos")
# ... resto de tu código de formulario ...
