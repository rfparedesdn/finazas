import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Mis Finanzas BA", page_icon="💰", layout="centered")

# --- ESTILO CSS PERSONALIZADO (Para los botones Monefy) ---
st.markdown("""
    <style>
    .stButton>button { width: 100%; border-radius: 50px; height: 3.5em; font-weight: bold; font-size: 18px; }
    div[data-testid="stExpander"] { border: none !important; box-shadow: none !important; }
    </style>
    """, unsafe_allow_headers=True)

# --- CREDENCIALES ---
# Uso la estructura que ya te funciona para limpiar la llave automáticamente
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
    
    # Leer datos para el gráfico
    data = sheet.get_all_records()
    df = pd.DataFrame(data)
except Exception as e:
    st.error(f"Error de conexión: {e}")
    st.stop()

# --- INTERFAZ ESTILO MONEFY ---
st.title("💸 Control de Gastos")

# Gráfico Central de Dona
if not df.empty and 'Monto' in df.columns:
    # Agrupar por categoría para el gráfico
    df_resumen = df.groupby('Categoría')['Monto'].sum().reset_index()
    
    fig = go.Figure(data=[go.Pie(
        labels=df_resumen['Categoría'], 
        values=df_resumen['Monto'], 
        hole=.7,
        marker=dict(colors=['#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', '#9966FF', '#C9CBCF']),
        textinfo='percent'
    )])
    fig.update_layout(showlegend=True, margin=dict(t=10, b=10, l=10, r=10), height=350)
    st.plotly_chart(fig, use_container_width=True)
    
    total_gastado = df_resumen['Monto'].sum()
    st.markdown(f"<h3 style='text-align: center;'>Total: ${total_gastado:,.2f}</h3>", unsafe_allow_headers=True)
else:
    st.info("Todavía no hay movimientos. ¡Cargá el primero abajo!")

# --- BOTONES DE ACCIÓN RÁPIDA ---
st.write("---")
col_ing, col_gas = st.columns(2)

# Categorías de tus imágenes
cat_gastos = ["Comida", "Transporte", "Alquiler", "Salud", "Ocio", "Servicios", "Mascotas", "Ropa", "Higiene", "Taxi"]
cat_ingresos = ["Salario", "Depósito", "Ahorros", "Otros"]

with col_ing:
    with st.expander("➕ INGRESO", expanded=False):
        with st.form("form_ingreso"):
            m_ing = st.number_input("Monto ($)", min_value=0.0, key="ing_val")
            c_ing = st.selectbox("Categoría", cat_ingresos)
            n_ing = st.text_input("Nota")
            if st.form_submit_button("Guardar Ingreso"):
                sheet.append_row([str(datetime.now().date()), c_ing, m_ing, n_ing, "Ingreso"])
                st.success("¡Ingreso guardado!")
                st.rerun()

with col_gas:
    with st.expander("➖ GASTO", expanded=False):
        with st.form("form_gasto"):
            m_gas = st.number_input("Monto ($)", min_value=0.0, key="gas_val")
            c_gas = st.selectbox("Categoría", cat_gastos)
            n_gas = st.text_input("Nota")
            if st.form_submit_button("Guardar Gasto"):
                sheet.append_row([str(datetime.now().date()), c_gas, m_gas, n_gas, "Gasto"])
                st.success("¡Gasto guardado!")
                st.rerun()

# --- TABLA DE ÚLTIMOS MOVIMIENTOS ---
if not df.empty:
    st.write("### Últimos Movimientos")
    st.dataframe(df.tail(10), use_container_width=True)



