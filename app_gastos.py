
# app_gastos.py
import streamlit as st
import json
import os
from datetime import datetime

st.set_page_config(page_title="Mis Finanzas", page_icon="💸", layout="wide")

DATA_DIR = "data"
os.makedirs(DATA_DIR, exist_ok=True)
fecha_actual = datetime.now().strftime("%Y-%m")
archivo_mes = os.path.join(DATA_DIR, f"{fecha_actual}.json")

def cargar_datos():
    if os.path.exists(archivo_mes):
        with open(archivo_mes, "r") as f:
            return json.load(f)
    else:
        return {
            "provisiones_mensuales": {
                "Ahorro": {"monto": 0, "provisionado": False},
                "Auto": {"monto": 30000, "provisionado": False},
                "Emergencias": {"monto": 0, "provisionado": False},
                "Pasajes": {"monto": 20000, "provisionado": False},
                "Remedios": {"monto": 100000, "provisionado": False},
                "Ropa": {"monto": 20000, "provisionado": False},
                "Mascotas": {"monto": 10000, "provisionado": False},
                "Gas": {"monto": 10000, "provisionado": False},
                "Eventos": {"monto": 0, "provisionado": False},
                "Leña": {"monto": 40000, "provisionado": False},
                "Cuotas": {"monto": 30000, "provisionado": False},
                "Arriendo": {"monto": 0, "provisionado": False},
                "💼 Sueldo próximo mes": {"monto": 0, "provisionado": False}
            }
        }

def guardar_datos(data):
    with open(archivo_mes, "w") as f:
        json.dump(data, f, indent=4)

st.title("💸 Control de Finanzas Personales - Sueldo Reservado")

datos = cargar_datos()

# Provisiones
st.header("🟦 Provisiones mensuales")
total_esperado = 0
total_real = 0
for nombre, info in datos["provisiones_mensuales"].items():
    col1, col2 = st.columns([4, 1])
    info["monto"] = col1.number_input(f"{nombre}", min_value=0, value=info["monto"], step=1000, key=f"prov_{nombre}")
    info["provisionado"] = col2.checkbox("✅ Provisionado", value=info["provisionado"], key=f"chk_{nombre}")
    total_esperado += info["monto"]
    if info["provisionado"]:
        total_real += info["monto"]

st.info(f"💼 Total esperado: ${total_esperado:,} — ✅ Total provisionado: ${total_real:,}")

if st.button("💾 Guardar mes"):
    guardar_datos(datos)
    st.success("✅ Datos guardados correctamente")
