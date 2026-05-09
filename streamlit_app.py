import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Mis Finanzas BA", page_icon="💰", layout="centered")

# --- CREDENCIALES (No toques tu llave, solo asegúrate que esté entre las comillas) ---
llave_cruda = """-----BEGIN PRIVATE KEY-----
MIIEvAIBADANBgkqhkiG9w0BAQEFAASCBKYwggSiAgEAAoIBAQC3SgBN+NH7mfC5\nUkKa56Lne+JtZaubLHlIxVXvxLiAZmI6H/OhdVqMVwMmjBNnkK2eSpf+HRHHT5+z\nka1d6xSxkgmRKlCoLmWUqxXIQNoNAueCwaCs8Baaqsbt57aec+64cJmxtEkRPXfv\nkzEfvlLi+p9oS1Em/pIUnPIRm2TpJqyGGORw3SgATtBtwvnfJrBO9hXPKsGC8a5S\nFWoGVygzwmcY3aKJkgKl9/YfJKcEGvXO4StFfqCxUSXiQQGZFWeMSFFTwRLJjUzP\nrGcayRE9mRvf6fZVHCuB3ED0awuhotvgGOTqr50Y1vvyDcylMEjIY8uHiD3bKw3b\neGJwZBxfAgMBAAECggEAQN90VCSpTcAir7Up1eH+iqgScF336yhGlTcjP4YFN40F\nX0VH2fHLZri1aMNTauiOSuRj/5ESZdUM1WXOUtuNq3vg3vx3J8+kLIaRYxtxEgHh\nJyqZUBx6I6wmVLYasOKfr7BK9da1teBnvuf+DxoyBBxop2VhB8g6tAkItKqngM2S\nB8c41Knae6RvDnliMUNGLeyEyKfN6JwffBBTg0YxnAOk0XJplcLXc8OlzbVkYsQg\nPqzae3fL8byjn/wRXg+WbldKALaGBwqoWOgl9ELLAVM6nSdlze4mMcHzWBzdoaVC\n4gMCbtN9p9U8tJuLPd3w5kDolvi7nNAR6qvqxs7VoQKBgQDeGD5ZYxWpDRNq90A4\neAkFukOIlS6VY6LNdTkz7tQZ9zzAlxlDzVCJSiP1oYe1P+8iJo62/1J2ploB6Jza\njL9iYtXlkwEtSpX+e5SUilbLGQRZoUsq28zAtaDbLoFSu+3GZ56zSIecCuOUoTqX\nSSMyj/+mN067rrPei4ewA3gLvQKBgQDTRS6LoQTpaaRu1XaFEh6Ze7m3rnqIYcTV\njzXU1/e4942LFJqH4InnS+bKZb08Xtn96wONp30ATvFuQ+W85hhuhBpYxTPWKQHR\nwSvVQKrJ0+cL9qQPREq8gyAae2/ny9msuKTgscM262Wlc8kZzBRXHLEl+hUECGb0\nCee4LbAcSwKBgH+XCeqsQ7tUqb0fwiMuwnAp67ZBjfuAu/ywxWYSZINuR9aUd40+\nHHBiyXnJjH8R9b12zTJQR/2l37uM+N+NUD2jbiJva5Orb7Q9JsSXHPmcq6UaRmae\n02g6b+i7NMxk7lq3GLMCjfWVQ90VKuXSvIfFtia1S2QDH45QNmll9Mc5AoGABaeC\nWWZT1VNofTblVyZm/0CaddoLmX7UX8rXa/zjumWVujUw9ZYC2tfjM2OJrwXy26Lg\nk3f6FnoGaCcVDPsziDGs6tdMTd0HGXAMFkcGyyQKuP0+4tG3FliEEXFgS1nfV4oR\nj5nyWZPvQoBYz4HwwWwZKaUJzvPSnZFuTDWc0wUCgYBTn2yxqjrdbe826GADcFsC\nkhswSvGDBcPzLz85xEUy73VY4xWKqwNOVZHv8pfR19sU04GVh2qkfXK1WhfsyRkP\nlBxudaOLWYL0H8aCK7eEMqk629TUFdw68ZaklkC00I2N1ixAKNC+Hm53Ktid1TWj\nmPl/Vp334oHDV89y2smIuQ==
-----END PRIVATE KEY-----"""

llave_fina = llave_cruda.replace("\\n", "\n").strip()

creds_dict = {
    "type": "service_account",
    "project_id": "capable-alcove-427523-u2",
    "private_key": llave_fina,
    "client_email": "gastos-bot@capable-alcove-427523-u2.iam.gserviceaccount.com",
    "token_uri": "https://oauth2.google.com/token",
}

# --- CONEXIÓN A GOOGLE SHEETS ---
try:
    scope = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
    creds = Credentials.from_service_account_info(creds_dict, scopes=scope)
    client = gspread.authorize(creds)
    sheet = client.open_by_key("1TBW_be5E2fhIJePzxKD_iL79ltP6-APE4EJKTaWTAvs").sheet1
    
    # Intentar leer datos
    data = sheet.get_all_records()
    df = pd.DataFrame(data)
except Exception as e:
    st.error(f"Error: {e}")
    st.stop()

# --- INTERFAZ ---
st.title("💸 Control de Gastos Rafael")

# Gráfico de Dona
if not df.empty:
    # Aseguramos que existan las columnas para que no explote
    if 'Categoría' in df.columns and 'Monto' in df.columns:
        resumen = df.groupby('Categoría')['Monto'].sum().reset_index()
        fig = go.Figure(data=[go.Pie(
            labels=resumen['Categoría'], 
            values=resumen['Monto'], 
            hole=.6,
            marker=dict(colors=['#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', '#9966FF'])
        )])
        fig.update_layout(margin=dict(t=0, b=0, l=0, r=0), height=300)
        st.plotly_chart(fig, use_container_width=True)
        
        total = resumen['Monto'].sum()
        st.metric("Gasto Total", f"${total:,.2f}")

st.write("---")

# Categorías de tus fotos
cat_gastos = ["Comida", "Transporte", "Alquiler", "Salud", "Ocio", "Servicios", "Mascotas", "Ropa", "Higiene", "Taxi"]

# Formulario simple sin el bloque CSS que dio error
with st.expander("➕ REGISTRAR NUEVO", expanded=True):
    with st.form("registro"):
        c1, c2 = st.columns(2)
        with c1:
            monto = st.number_input("Monto ($)", min_value=0.0, step=100.0)
            categoria = st.selectbox("Categoría", cat_gastos)
        with c2:
            fecha = st.date_input("Fecha", datetime.now())
            nota = st.text_input("Nota")
        
        btn = st.form_submit_button("GUARDAR EN EXCEL")
        
        if btn and monto > 0:
            # Agregamos: Fecha, Categoría, Monto, Nota
            sheet.append_row([str(fecha), categoria, monto, nota])
            st.success("¡Guardado!")
            st.balloons()
            st.rerun()

# Historial
if not df.empty:
    st.write("### Últimos movimientos")
    st.dataframe(df.tail(5), use_container_width=True)


