import streamlit as st
import gspread
from google.oauth2.service_account import Credentials

# 1. PEGA TU LLAVE AQUÍ
# Asegurate de que NO haya nada después de los últimos 5 guiones
llave_cruda = """-----BEGIN PRIVATE KEY-----
MIIEvAIBADANBgkqhkiG9w0BAQEFAASCBKYwggSiAgEAAoIBAQC3SgBN+NH7mfC5UkKa56Lne+JtZaubLHlIxVXvxLiAZmI6H/OhdVqMVwMmjBNnkK2eSpf+HRHHT5+zka1d6xSxkgmRKlCoLmWUqxXIQNoNAueCwaCs8Baaqsbt57aec+64cJmxtEkRPXfvkzEfvlLi+p9oS1Em/pIUnPIRm2TpJqyGGORw3SgATtBtwvnfJrBO9hXPKsGC8a5SFWoGVygzwmcY3aKJkgKl9/YfJKcEGvXO4StFfqCxUSXiQQGZFWeMSFFTwRLJjUzP\nrGcayRE9mRvf6fZVHCuB3ED0awuhotvgGOTqr50Y1vvyDcylMEjIY8uHiD3bKw3beGJwZBxfAgMBAAECggEAQN90VCSpTcAir7Up1eH+iqgScF336yhGlTcjP4YFN40FX0VH2fHLZri1aMNTauiOSuRj/5ESZdUM1WXOUtuNq3vg3vx3J8+kLIaRYxtxEgHhJyqZUBx6I6wmVLYasOKfr7BK9da1teBnvuf+DxoyBBxop2VhB8g6tAkItKqngM2SB8c41Knae6RvDnliMUNGLeyEyKfN6JwffBBTg0YxnAOk0XJplcLXc8OlzbVkYsQgPqzae3fL8byjn/wRXg+WbldKALaGBwqoWOgl9ELLAVM6nSdlze4mMcHzWBzdoaVC4gMCbtN9p9U8tJuLPd3w5kDolvi7nNAR6qvqxs7VoQKBgQDeGD5ZYxWpDRNq90A4eAkFukOIlS6VY6LNdTkz7tQZ9zzAlxlDzVCJSiP1oYe1P+8iJo62/1J2ploB6JzajL9iYtXlkwEtSpX+e5SUilbLGQRZoUsq28zAtaDbLoFSu+3GZ56zSIecCuOUoTqX\nSSMyj/+mN067rrPei4ewA3gLvQKBgQDTRS6LoQTpaaRu1XaFEh6Ze7m3rnqIYcTV\njzXU1/e4942LFJqH4InnS+bKZb08Xtn96wONp30ATvFuQ+W85hhuhBpYxTPWKQHR\nwSvVQKrJ0+cL9qQPREq8gyAae2y9msuKTgscM262Wlc8kZzBRXHLEl+hUECGb0\nCee4LbAcSwKBgH+XCeqsQ7tUqb0fwiMuwnAp67ZBjfuAu/ywxWYSZINuR9aUd40+HHBiyXnJjH8R9b12zTJQR/2l37uM+N+NUD2jbiJva5Orb7Q9JsSXHPmcq6UaRmae02g6b+i7NMxk7lq3GLMCjfWVQ90VKuXSvIfFtia1S2QDH45QNmll9Mc5AoGABaeCWWZT1VNofTblVyZm/0CaddoLmX7UX8rXa/zjumWVujUw9ZYC2tfjM2OJrwXy26Lg\nk3f6FnoGaCcVDPsziDGs6tdMTd0HGXAMFkcGyyQKuP0+4tG3FliEEXFgS1nfV4oRj5nyWZPvQoBYz4HwwWwZKaUJzvPSnZFuTDWc0wUCgYBTn2yxqjrdbe826GADcFsCkhswSvGDBcPzLz85xEUy73VY4xWKqwNOVZHv8pfR19sU04GVh2qkfXK1WhfsyRkPlBxudaOLWYL0H8aCK7eEMqk629TUFdw68ZaklkC00I2N1ixAKNC+Hm53Ktid1TWjmPl/Vp334oHDV89y2smIuQ==
-----END PRIVATE KEY-----"""

# 2. LIMPIEZA TOTAL (Esto borra cualquier ") o \n que se cuele)
llave_limpia = llave_cruda.replace("\\n", "\n").strip()

creds_dict = {
    "type": "service_account",
    "project_id": "capable-alcove-427523-u2",
    "private_key_id": "78e3a250f0c20b6a409b10076992ba6b86e4f5ed",
    "private_key": llave_limpia,
    "client_email": "gastos-bot@capable-alcove-427523-u2.iam.gserviceaccount.com",
    "client_id": "111847215780906508573",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.google.com/token",
}

try:
    scope = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
    creds = Credentials.from_service_account_info(creds_dict, scopes=scope)
    client = gspread.authorize(creds)
    sheet = client.open_by_key("1TBW_be5E2fhIJePzxKD_iL79ltP6-APE4EJKTaWTAvs").sheet1
    st.success("✅ ¡CONECTADO!")
    
    with st.form("gastos"):
        concepto = st.text_input("Gasto")
        monto = st.number_input("Precio", min_value=0)
        if st.form_submit_button("Guardar"):
            sheet.append_row([concepto, monto])
            st.balloons()
except Exception as e:
    st.error(f"Error: {e}")
