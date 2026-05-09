import streamlit as st
import gspread
from google.oauth2.service_account import Credentials

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Riqueza Rafael", page_icon="💰")

# --- LA LLAVE (Ya está integrada y limpia) ---
llave = """-----BEGIN PRIVATE KEY-----
MIIEvAIBADANBgkqhkiG9w0BAQEFAASCBKYwggSiAgEAAoIBAQC3SgBN+NH7mfC5
UkKa56Lne+JtZaubLHlIxVXvxLiAZmI6H/OhdVqMVwMmjBNnkK2eSpf+HRHHT5+z
ka1d6xSxkgmRKlCoLmWUqxXIQNoNAueCwaCs8Baaqsbt57aec+64cJmxtEkRPXfv
kzEfvlLi+p9oS1Em/pIUnPIRm2TpJqyGGORw3SgATtBtwvnfJrBO9hXPKsGC8a5S
FWoGVygzwmcY3aKJkgKl9/YfJKcEGvXO4StFfqCxUSXiQQGZFWeMSFFTwRLJjUzP
rGcayRE9mRvf6fZVHCuB3ED0awuhotvgGOTqr50Y1vvyDcylMEjIY8uHiD3bKw3b
eGJwZBxfAgMBAAECggEAQN90VCSpTcAir7Up1eH+iqgScF336yhGlTcjP4YFN40F
X0VH2fHLZri1aMNTauiOSuRj/5ESZdUM1WXOUtuNq3vg3vx3J8+kLIaRYxtxEgHh
JyqZUBx6I6wmVLYasOKfr7BK9da1teBnvuf+DxoyBBxop2VhB8g6tAkItKqngM2S
B8c41Knae6RvDnliMUNGLeyEyKfN6JwffBBTg0YxnAOk0XJplcLXc8OlzbVkYsQg
Pqzae3fL8byjn/wRXg+WbldKALaGBwqoWOgl9ELLAVM6nSdlze4mMcHzWBzdoaVC
4gMCbtN9p9U8tJuLPd3w5kDolvi7nNAR6qvqxs7VoQKBgQDeGD5ZYxWpDRNq90A4
eAkFukOIlS6VY6LNdTkz7tQZ9zzAlxlDzVCJSiP1oYe1P+8iJo62/1J2ploB6Jza
jL9iYtXlkwEtSpX+e5SUilbLGQRZoUsq28zAtaDbLoFSu+3GZ56zSIecCuOUoTqX
SSMyj/+mN067rrPei4ewA3gLvQKBgQDTRS6LoQTpaaRu1XaFEh6Ze7m3rnqIYcTV
jzXU1/e4942LFJqH4InnS+bKZb08Xtn96wONp30ATvFuQ+W85hhuhBpYxTPWKQHR
wSvVQKrJ0+cL9qQPREq8gyAae2/ny9msuKTgscM262Wlc8kZzBRXHLEl+hUECGb0
Cee4LbAcSwKBgH+XCeqsQ7tUqb0fwiMuwnAp67ZBjfuAu/ywxWYSZINuR9aUd40+
HHBiyXnJjH8R9b12zTJQR/2l37uM+N+NUD2jbiJva5Orb7Q9JsSXHPmcq6UaRmae
02g6b+i7NMxk7lq3GLMCjfWVQ90VKuXSvIfFtia1S2QDH45QNmll9Mc5AoGABaeC
WWZT1VNofTblVyZm/0CaddoLmX7UX8rXa/zjumWVujUw9ZYC2tfjM2OJrwXy26Lg
k3f6FnoGaCcVDPsziDGs6tdMTd0HGXAMFkcGyyQKuP0+4tG3FliEEXFgS1nfV4oR
j5nyWZPvQoBYz4HwwWwZKaUJzvPSnZFuTDWc0wUCgYBTn2yxqjrdbe826GADcFsC
khswSvGDBcPzLz85xEUy73VY4xWKqwNOVZHv8pfR19sU04GVh2qkfXK1WhfsyRkP
lBxudaOLWYL0H8aCK7eEMqk629TUFdw68ZaklkC00I2N1ixAKNC+Hm53Ktid1TWj
mPl/Vp334oHDV89y2smIuQ==
-----END PRIVATE KEY-----"""

# Estructura de credenciales
info = {
    "type": "service_account",
    "project_id": "capable-alcove-427523-u2",
    "private_key": llave.replace('\\n', '\n'),
    "client_email": "gastos-bot@capable-alcove-427523-u2.iam.gserviceaccount.com",
    "token_uri": "https://oauth2.google.com/token",
}

try:
    # Autenticación
    scope = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
    creds = Credentials.from_service_account_info(info, scopes=scope)
    client = gspread.authorize(creds)
    
    # Abrir el Excel
    sh = client.open_by_key("1TBW_be5E2fhIJePzxKD_iL79ltP6-APE4EJKTaWTAvs")
    hoja = sh.get_worksheet(0) # Esto toma la primera pestaña (Hoja 1)

    st.title("💰 Control de Gastos - Rafael")
    st.markdown("---")

    # Formulario de entrada
    with st.form("nuevo_gasto", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            categoria = st.selectbox("Categoría", ["🍔 Comida", "🚕 Transporte", "💊 Salud", "🏠 Hogar", "✨ Varios"])
        with col2:
            monto = st.number_input("Monto ($)", min_value=0, step=100)
        
        detalle = st.text_input("¿Qué compraste?")
        enviar = st.form_submit_button("REGISTRAR GASTO")

        if enviar:
            if monto > 0:
                # Escribir en el Excel: Fecha, Categoría, Monto, Detalle
                import datetime
                fecha = datetime.datetime.now().strftime("%d/%m/%Y")
                hoja.append_row([fecha, categoria, monto, detalle])
                
                st.success(f"¡Listo! Se guardaron ${monto} en {categoria}")
                st.balloons()
            else:
                st.warning("Por favor, ingresá un monto mayor a 0.")

except Exception as e:
    st.error("Error de conexión:")
    st.code(str(e))
    st.info("Asegúrate de que el bot sea 'Editor' en tu Google Sheet.")
