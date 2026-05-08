import sqlite3
from datetime import datetime

# Configuración de la base de datos
def iniciar_db():
    conn = sqlite3.connect('finanzas.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS movimientos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tipo TEXT,
            categoria TEXT,
            monto_ars REAL,
            monto_usd REAL,
            descripcion TEXT,
            fecha TEXT
        )
    ''')
    conn.commit()
    return conn

def registrar_movimiento(tipo, categoria, ars, usd, desc):
    conn = iniciar_db()
    cursor = conn.cursor()
    fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute('''
        INSERT INTO movimientos (tipo, categoria, monto_ars, monto_usd, descripcion, fecha)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (tipo, categoria, ars, usd, desc, fecha))
    conn.commit()
    conn.close()
    print(f"\n✅ {tipo} registrado con éxito.")

def mostrar_resumen():
    conn = iniciar_db()
    cursor = conn.cursor()
    cursor.execute("SELECT SUM(monto_ars), SUM(monto_usd) FROM movimientos WHERE tipo='Ingreso'")
    ingresos = cursor.fetchone()
    cursor.execute("SELECT SUM(monto_ars), SUM(monto_usd) FROM movimientos WHERE tipo='Gasto'")
    gastos = cursor.fetchone()
    conn.close()

    i_ars = ingresos[0] or 0
    i_usd = ingresos[1] or 0
    g_ars = gastos[0] or 0
    g_usd = gastos[1] or 0

    print("\n--- RESUMEN DE CUENTA ---")
    print(f"Total Ingresos: ${i_ars:,.2f} ARS | {i_usd:,.2f} USD")
    print(f"Total Gastos:   ${g_ars:,.2f} ARS | {g_usd:,.2f} USD")
    print(f"SALDO ACTUAL:   ${(i_ars - g_ars):,.2f} ARS | {(i_usd - g_usd):,.2f} USD")
    print("------------------------\n")

def menu():
    iniciar_db()
    while True:
        print("1. Registrar Ingreso (Uber/Otros)")
        print("2. Registrar Gasto (Comida, Transporte, Mensualidad, etc.)")
        print("3. Ver Resumen")
        print("4. Salir")
        opcion = input("Elegí una opción: ")

        if opcion == "1":
            desc = input("Descripción: ")
            ars = float(input("Monto en ARS: "))
            usd = float(input("Monto en USD (0 si no aplica): "))
            registrar_movimiento("Ingreso", "General", ars, usd, desc)
        
        elif opcion == "2":
            print("\nCategorías: 1. Comida | 2. Transporte | 3. Mensualidad | 4. Otro")
            cat_op = input("Elegí categoría: ")
            categorias = {"1": "Comida", "2": "Transporte", "3": "Mensualidad", "4": "Otro"}
            cat = categorias.get(cat_op, "Otro")
            
            desc = input("Descripción: ")
            ars = float(input("Monto en ARS: "))
            usd = float(input("Monto en USD (0 si no aplica): "))
            registrar_movimiento("Gasto", cat, ars, usd, desc)

        elif opcion == "3":
            mostrar_resumen()
        
        elif opcion == "4":
            break

if __name__ == "__main__":
    menu()