
# app_gastos.py
import streamlit as st
import json
import os
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Mis Finanzas", page_icon="💸", layout="wide")

# Crear carpeta de datos
DATA_DIR = "data"
os.makedirs(DATA_DIR, exist_ok=True)

# Fecha actual
fecha_actual = datetime.now().strftime("%Y-%m")
archivo_mes = os.path.join(DATA_DIR, f"{fecha_actual}.json")

# ---------- Funciones ----------
def cargar_datos():
    if os.path.exists(archivo_mes):
        with open(archivo_mes, "r") as f:
            return json.load(f)
    else:
        return {
            "ingresos_fijos": {
                "Sueldo AIEP": 0,
                "Pensión hijo": 0,
                "Seguro cesantía": 0
            },
            "ingresos_correos": [],
            "ingresos_otros": [],
            "ahorro_hijos": {
                "Sebastián": {"auto": 5000, "extra": []},
                "Hernán": {"auto": 5000, "extra": []},
                "Mailen": {"auto": 5000, "extra": []}
            },
            "deudas": {
                "Santander": {"monto": 41128, "pagadas": 9, "total": 120, "pagado": False},
                "Scotiabank": {"monto": 272060, "pagadas": 9, "total": 120, "pagado": False},
                "Cencosud": {"monto": 163179, "pagadas": 9, "total": 120, "pagado": False},
                "Ripley": {"monto": 28419, "pagadas": 9, "total": 120, "pagado": False},
                "Falabella": {"monto": 14743, "pagadas": 9, "total": 120, "pagado": False}
            },
            "gastos_fijos": {
                "Arriendo": {"monto": 350000, "pagado": False},
                "Luz": {"monto": 70000, "pagado": False},
                "Agua": {"monto": 35000, "pagado": False},
                "Teléfono Entel": {"monto": 210000, "pagado": False},
                "Teléfono Wom": {"monto": 15000, "pagado": False},
                "Internet (Tenpo)": {"monto": 32000, "pagado": False},
                "Cable (Tenpo)": {"monto": 30000, "pagado": False},
                "Netflix (Tenpo)": {"monto": 13000, "pagado": False},
                "YouTube Premium (Tenpo)": {"monto": 10000, "pagado": False},
                "Disney+ (Tenpo)": {"monto": 10000, "pagado": False},
                "Spotify (Tenpo)": {"monto": 7050, "pagado": False},
                "ChatGPT (Tenpo)": {"monto": 20000, "pagado": False},
                "Otros Play Store (Tenpo)": {"monto": 40000, "pagado": False},
                "Bencina (Copec Pay)": {"monto": 150000, "pagado": False},
                "Mercadería (cuenta separada)": {"monto": 750000, "pagado": False}
            }
        }

def guardar_datos(data):
    with open(archivo_mes, "w") as f:
        json.dump(data, f, indent=4)

# ---------- Interfaz ----------
st.title("💸 Control de Finanzas Personales")
datos = cargar_datos()

# Ahorro hijos
st.header("👶 Ahorros para los hijos")
total_ahorro = 0
for hijo, info in datos["ahorro_hijos"].items():
    col1, col2 = st.columns([3, 1])
    col1.write(f"**{hijo}** - Ahorro automático: ${info['auto']}")
    extra = col1.number_input(f"Ahorro extra para {hijo}", min_value=0, step=1000, key=f"{hijo}_extra")
    if col2.button(f"➕ Agregar ahorro extra - {hijo}", key=f"{hijo}_btn"):
        info["extra"].append(extra)
    total_ahorro += info["auto"] + sum(info["extra"])
    st.write(f"Ahorro total este mes para {hijo}: ${info['auto'] + sum(info['extra']):,}")

st.success(f"💖 Total ahorro hijos este mes: ${total_ahorro:,}")

# Guardar
if st.button("💾 Guardar mes"):
    guardar_datos(datos)
    st.success("✅ Datos guardados correctamente")
