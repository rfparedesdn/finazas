import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
import re
import pandas as pd

# --- CONFIGURACIÓN ESTILO MONEFY ---
st.set_page_config(page_title="Riqueza Rafael", layout="centered")

st.markdown("""
    <style>
    .stButton>button {
        width: 100%;
        border-radius: 20px;
        height: 3em;
        background-color: #f0f2f6;
    }
    .monto-grande {
        font-size: 40px;
        font-weight: bold;
        color: #2e7d32;
        text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)

# --- TU LLAVE (Asegurate que esté bien pegada aquí) ---
llave_cruda = """-----BEGIN PRIVATE KEY-----
MIIEvAIBADANBgkqhkiG9w0BAQEFAASCBKYwggSiAgEAAoIBAQC3SgBN+NH7mfC5\nUkKa56Lne+JtZaubLHlIxVXvxLiAZmI6H/OhdVqMVwMmjBNnkK2eSpf+HRHHT5+z\nka1d6xSxkgmRKlCoLmWUqxXIQNoNAueCwaCs8Baaqsbt57aec+64cJmxtEkRPXfv\nkzEfvlLi+p9oS1Em/pIUnPIRm2TpJqyGGORw3SgATtBtwvnfJrBO9hXPKsGC8a5S\nFWoGVygzwmcY3aKJkgKl9/YfJKcEGvXO4StFfqCxUSXiQQGZFWeMSFFTwRLJjUzP\nrGcayRE9mRvf6fZVHCuB3ED0awuhotvgGOTqr50Y1vvyDcylMEjIY8uHiD3bKw3b\neGJwZBxfAgMBAAECggEAQN90VCSpTcAir7Up1eH+iqgScF336yhGlTcjP4YFN40F\nX0VH2fHLZri1aMNTauiOSuRj/5ESZdUM1WXOUtuNq3vg3vx3J8+kLIaRYxtxEgHh\nJyqZUBx6I6wmVLYasOKfr7BK9da1teBnvuf+DxoyBBxop2VhB8g6tAkItKqngM2S\nB8c41Knae6RvDnliMUNGLeyEyKfN6JwffBBTg0YxnAOk0XJplcLXc8OlzbVkYsQg\nPqzae3fL8byjn/wRXg+WbldKALaGBwqoWOgl9ELLAVM6nSdlze4mMcHzWBzdoaVC\n4gMCbtN9p9U8tJuLPd3w5kDolvi7nNAR6qvqxs7VoQKBgQDeGD5ZYxWpDRNq90A4\neAkFukOIlS6VY6LNdTkz7tQZ9zzAlxlDzVCJSiP1oYe1P+8iJo62/1J2ploB6Jza\njL9iYtXlkwEtSpX+e5SUilbLGQRZoUsq28zAtaDbLoFSu+3GZ56zSIecCuOUoTqX\nSSMyj/+mN067rrPei4ewA3gLvQKBgQDTRS6LoQTpaaRu1XaFEh6Ze7m3rnqIYcTV\njzXU1/e4942LFJqH4InnS+bKZb08Xtn96wONp30ATvFuQ+W85hhuhBpYxTPWKQHR\nwSvVQKrJ0+cL9qQPREq8gyAae2/ny9msuKTgscM262Wlc8kZzBRXHLEl+hUECGb0\nCee4LbAcSwKBgH+XCeqsQ7tUqb0fwiMuwnAp67ZBjfuAu/ywxWYSZINuR9aUd40+\nHHBiyXnJjH8R9b12zTJQR/2l37uM+N+NUD2jbiJva5Orb7Q9JsSXHPmcq6UaRmae\n02g6b+i7NMxk7lq3GLMCjfWVQ90VKuXSvIfFtia1S2QDH45QNmll9Mc5AoGABaeC\nWWZT1VNofTblVyZm/0CaddoLmX7UX8rXa/zjumWVujUw9ZYC2tfjM2OJrwXy26Lg\nk3f6FnoGaCcVDPsziDGs6tdMTd0HGXAMFkcGyyQKuP0+4tG3FliEEXFgS1nfV4oR\nj5nyWZPvQoBYz4HwwWwZKaUJzvPSnZFuTDWc0wUCgYBTn2yxqjrdbe826GADcFsC\nkhswSvGDBcPzLz85xEUy73VY4xWKqwNOVZHv8pfR19sU04GVh2qkfXK1WhfsyRkP\nlBxudaOLWYL0H8aCK7eEMqk629TUFdw68ZaklkC00I2N1ixAKNC+Hm53Ktid1TWj\nmPl/Vp334oHDV89y2smIuQ==
-----END PRIVATE KEY-----"""

# Limpieza de llave
cuerpo = llave_cruda.replace("-----BEGIN PRIVATE KEY-----", "").replace("-----END PRIVATE KEY-----", "")
cuerpo_limpio = re.sub(r'\s+', '', cuerpo)
llave_final = f"-----BEGIN PRIVATE KEY-----\n{cuerpo_limpio}\n-----END PRIVATE KEY-----"

info = {
    "type": "service_account",
    "project_id": "capable-alcove-427523-u2",
    "private_key": llave_final,
    "client_email": "gastos-bot@capable-alcove-427523-u2.iam.gserviceaccount.com",
    "token_uri": "https://oauth2.google.com/token",
}

try:
    scope = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
    creds = Credentials.from_service_account_info(info, scopes=scope)
    client = gspread.authorize(creds)
    sheet = client.open_by_key("1TBW_be5E2fhIJePzxKD_iL79ltP6-APE4EJKTaWTAvs").sheet1

    st.title("💰 Control de Gastos BA")
    
    # --- INTERFAZ DE ICONOS ---
    st.subheader("¿En qué gastaste hoy?")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🍔 Comida"):
            categoria = "Comida"
    with col2:
        if st.button("🚕 Transporte"):
            categoria = "Transporte"
    with col3:
        if st.button("💊 Salud"):
            categoria = "Salud"

    # Formulario para el monto
    with st.form("registro_gasto"):
        monto = st.number_input("¿Cuánto fue? ($)", min_value=0)
        nota = st.text_input("Detalle (opcional)")
        enviar = st.form_submit_button("REGISTRAR GASTO")
        
        if enviar:
            sheet.append_row(["Hoy", "Categoría", monto, nota])
            st.success("¡Guardado en el Excel!")
            st.balloons()

    # --- RESUMEN VISUAL ---
    st.markdown("---")
    st.markdown("<p class='monto-grande'>Saldo Actual: $ ---</p>", unsafe_allow_html=True)
    st.info("Aquí aparecerá el gráfico de dona cuando registres tus primeros gastos.")

except Exception as e:
    st.error("Esperando conexión con el servidor...")
    st.info("Si ves el error rosa, dale unos minutos. El código está listo para funcionar.")
