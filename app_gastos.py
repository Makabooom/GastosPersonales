
# app_gastos.py
import streamlit as st
import json
import os
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Gastos Personales", page_icon="💸")

# Archivos
archivo_actual = "gastos_actual.json"
archivo_historico = "gastos_historico.json"
archivo_excel = "gastos_historico.xlsx"

# Categorías base
categorias_defecto = {
    "Auto": 30000,
    "Emergencias": 0,
    "Pasajes": 40000,
    "Remedios": 20000,
    "Ropa": 0
}

# Cargar datos actuales
if os.path.exists(archivo_actual):
    with open(archivo_actual, "r") as f:
        datos = json.load(f)
        sueldo = datos.get("sueldo", 0)
        categorias = datos.get("categorias", categorias_defecto.copy())
else:
    sueldo = 0
    categorias = categorias_defecto.copy()

# Título
st.title("💸 App de Gastos Personales")
st.markdown("Visualiza, ajusta y guarda tus ahorros mensuales.")

# Sueldo
sueldo = st.number_input("💰 Sueldo mensual", min_value=0, value=sueldo, step=1000)

# Categorías
st.subheader("🏷️ Ahorros por categoría")
total = 0
for cat in categorias:
    nuevo = st.number_input(cat, min_value=0, value=categorias[cat], step=1000)
    categorias[cat] = nuevo
    total += nuevo

# Saldo disponible
saldo = sueldo - total
st.markdown(f"### 💵 Saldo disponible: **${saldo:,}**")
if saldo < 0:
    st.error("🚨 ¡Estás gastando más de lo que ganas!")

# Gráfico
st.subheader("📊 Distribución")
df = pd.DataFrame(categorias.items(), columns=["Categoría", "Monto"])
st.bar_chart(df.set_index("Categoría"))

# Guardar actual e histórico
if st.button("💾 Guardar este mes"):
    # Guardar actual
    with open(archivo_actual, "w") as f:
        json.dump({
            "fecha": datetime.now().strftime("%Y-%m-%d"),
            "sueldo": sueldo,
            "categorias": categorias
        }, f)

    # Agregar al histórico
    historial = []
    if os.path.exists(archivo_historico):
        with open(archivo_historico, "r") as f:
            historial = json.load(f)

    historial.append({
        "fecha": datetime.now().strftime("%Y-%m-%d"),
        "sueldo": sueldo,
        "categorias": categorias
    })

    with open(archivo_historico, "w") as f:
        json.dump(historial, f)

    st.success("✅ Datos guardados y añadido al historial.")

# Mostrar historial
if os.path.exists(archivo_historico):
    st.subheader("📅 Historial de meses anteriores")
    with open(archivo_historico, "r") as f:
        historial = json.load(f)

    tabla = []
    for item in historial:
        fila = {"Fecha": item["fecha"], "Sueldo": item["sueldo"]}
        fila.update(item["categorias"])
        tabla.append(fila)

    df_hist = pd.DataFrame(tabla)
    st.dataframe(df_hist)

    # Exportar a Excel
    if st.button("📤 Exportar historial a Excel"):
        df_hist.to_excel(archivo_excel, index=False)
        with open(archivo_excel, "rb") as f:
            st.download_button("⬇️ Descargar Excel", data=f, file_name="historial_gastos.xlsx")
