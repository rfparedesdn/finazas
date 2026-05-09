import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
import re

# 1. PEGA TU LLAVE AQUÍ (No importa si tiene espacios o \n)
llave_cruda = """-----BEGIN PRIVATE KEY-----
MIIEvAIBADANBgkqhkiG9w0BAQEFAASCBKYwggSiAgEAAoIBAQC3SgBN+NH7mfC5\nUkKa56Lne+JtZaubLHlIxVXvxLiAZmI6H/OhdVqMVwMmjBNnkK2eSpf+HRHHT5+z\nka1d6xSxkgmRKlCoLmWUqxXIQNoNAueCwaCs8Baaqsbt57aec+64cJmxtEkRPXfv\nkzEfvlLi+p9oS1Em/pIUnPIRm2TpJqyGGORw3SgATtBtwvnfJrBO9hXPKsGC8a5S\nFWoGVygzwmcY3aKJkgKl9/YfJKcEGvXO4StFfqCxUSXiQQGZFWeMSFFTwRLJjUzP\nrGcayRE9mRvf6fZVHCuB3ED0awuhotvgGOTqr50Y1vvyDcylMEjIY8uHiD3bKw3b\neGJwZBxfAgMBAAECggEAQN90VCSpTcAir7Up1eH+iqgScF336yhGlTcjP4YFN40F\nX0VH2fHLZri1aMNTauiOSuRj/5ESZdUM1WXOUtuNq3vg3vx3J8+kLIaRYxtxEgHh\nJyqZUBx6I6wmVLYasOKfr7BK9da1teBnvuf+DxoyBBxop2VhB8g6tAkItKqngM2S\nB8c41Knae6RvDnliMUNGLeyEyKfN6JwffBBTg0YxnAOk0XJplcLXc8OlzbVkYsQg\nPqzae3fL8byjn/wRXg+WbldKALaGBwqoWOgl9ELLAVM6nSdlze4mMcHzWBzdoaVC\n4gMCbtN9p9U8tJuLPd3w5kDolvi7nNAR6qvqxs7VoQKBgQDeGD5ZYxWpDRNq90A4\neAkFukOIlS6VY6LNdTkz7tQZ9zzAlxlDzVCJSiP1oYe1P+8iJo62/1J2ploB6Jza\njL9iYtXlkwEtSpX+e5SUilbLGQRZoUsq28zAtaDbLoFSu+3GZ56zSIecCuOUoTqX\nSSMyj/+mN067rrPei4ewA3gLvQKBgQDTRS6LoQTpaaRu1XaFEh6Ze7m3rnqIYcTV\njzXU1/e4942LFJqH4InnS+bKZb08Xtn96wONp30ATvFuQ+W85hhuhBpYxTPWKQHR\nwSvVQKrJ0+cL9qQPREq8gyAae2/ny9msuKTgscM262Wlc8kZzBRXHLEl+hUECGb0\nCee4LbAcSwKBgH+XCeqsQ7tUqb0fwiMuwnAp67ZBjfuAu/ywxWYSZINuR9aUd40+\nHHBiyXnJjH8R9b12zTJQR/2l37uM+N+NUD2jbiJva5Orb7Q9JsSXHPmcq6UaRmae\n02g6b+i7NMxk7lq3GLMCjfWVQ90VKuXSvIfFtia1S2QDH45QNmll9Mc5AoGABaeC\nWWZT1VNofTblVyZm/0CaddoLmX7UX8rXa/zjumWVujUw9ZYC2tfjM2OJrwXy26Lg\nk3f6FnoGaCcVDPsziDGs6tdMTd0HGXAMFkcGyyQKuP0+4tG3FliEEXFgS1nfV4oR\nj5nyWZPvQoBYz4HwwWwZKaUJzvPSnZFuTDWc0wUCgYBTn2yxqjrdbe826GADcFsC\nkhswSvGDBcPzLz85xEUy73VY4xWKqwNOVZHv8pfR19sU04GVh2qkfXK1WhfsyRkP\nlBxudaOLWYL0H8aCK7eEMqk629TUFdw68ZaklkC00I2N1ixAKNC+Hm53Ktid1TWj\nmPl/Vp334oHDV89y2smIuQ==
-----END PRIVATE KEY-----"""

# --- PROCESO DE LIMPIEZA ---
# Esto quita cualquier cosa que no sea la llave real
cuerpo = llave_cruda.replace("-----BEGIN PRIVATE KEY-----", "").replace("-----END PRIVATE KEY-----", "")
cuerpo_limpio = re.sub(r'\s+', '', cuerpo) # Borra espacios y saltos de línea
llave_final = f"-----BEGIN PRIVATE KEY-----\n{cuerpo_limpio}\n-----END PRIVATE KEY-----"

# Diccionario con nombres en INGLÉS (Fundamental para Google)
creds_dict = {
    "type": "service_account",
    "project_id": "capable-alcove-427523-u2",
    "private_key_id": "78e3a250f0c20b6a409b10076992ba6b86e4f5ed",
    "private_key": llave_final,
    "client_email": "gastos-bot@capable-alcove-427523-u2.iam.gserviceaccount.com",
    "client_id": "111847215780906508573",
    "token_uri": "https://oauth2.google.com/token",
}

st.title("💰 Control de Gastos")

try:
    scope = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
    creds = Credentials.from_service_account_info(creds_dict, scopes=scope)
    client = gspread.authorize(creds)
    # Tu ID de Excel
    sheet = client.open_by_key("1TBW_be5E2fhIJePzxKD_iL79ltP6-APE4EJKTaWTAvs").sheet1
    st.success("✅ ¡CONECTADO CON ÉXITO!")

    # Formulario básico
    with st.form("registro"):
        detalle = st.text_input("¿En qué gastaste?")
        monto = st.number_input("Monto ($)", min_value=0)
        if st.form_submit_button("Guardar"):
            sheet.append_row([detalle, monto])
            st.balloons()
            st.success("¡Guardado!")

except Exception as e:
    st.error(f"Error: {e}")





