import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Título de la aplicación
st.title("Mi Control de Finanzas Personal")

# Entrada de datos en la barra lateral
st.sidebar.header("Registrar Ahorros")
categoria = st.sidebar.selectbox("Categoría", ["Efectivo", "Inversiones (CEDEARs)", "DolarApp", "Otros"])
monto = st.sidebar.number_input("Monto", min_value=0.0, step=100.0)

# Botón para simular carga de datos
if st.sidebar.button("Agregar Registro"):
    st.sidebar.success(f"Cargaste {monto} en {categoria}")

# Ejemplo de visualización
st.subheader("Resumen de Mis Ahorros")

# Creamos una tabla ficticia para ver cómo se vería
data = {
    'Categoría': ['Efectivo', 'Inversiones', 'DolarApp'],
    'Monto': [50000, 120000, 85000] # Estos son valores de ejemplo
}
df = pd.DataFrame(data)

# Mostrar la tabla
st.table(df)

# Mostrar un gráfico de barras
st.bar_chart(df.set_index('Categoría'))

st.info("Podes modificar este código más adelante para conectar tu base de datos real.")