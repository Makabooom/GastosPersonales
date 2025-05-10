
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

# INGRESOS
st.header("📥 Ingresos")
cols = st.columns(3)
for i, key in enumerate(datos["ingresos_fijos"]):
    datos["ingresos_fijos"][key] = cols[i % 3].number_input(key, value=datos["ingresos_fijos"][key], min_value=0)

st.subheader("💌 Ingresos por correos")
st.write(f"Total: ${sum(datos['ingresos_correos']):,}")
nuevo_correo = st.number_input("Agregar ingreso por correos", min_value=0, step=1000)
if st.button("➕ Agregar ingreso correo"):
    datos["ingresos_correos"].append(nuevo_correo)

st.subheader("🎁 Otros ingresos")
st.write(f"Total: ${sum(datos['ingresos_otros']):,}")
nuevo_otro = st.number_input("Agregar otro ingreso", min_value=0, step=1000)
if st.button("➕ Agregar otro ingreso"):
    datos["ingresos_otros"].append(nuevo_otro)

total_ingresos = sum(datos["ingresos_fijos"].values()) + sum(datos["ingresos_correos"]) + sum(datos["ingresos_otros"])
st.success(f"🧮 Total ingresos del mes: ${total_ingresos:,}")

# DEUDAS
st.header("💳 Deudas")
for deuda, info in datos["deudas"].items():
    col1, col2, col3 = st.columns([3, 2, 1])
    col1.write(f"**{deuda}**: ${info['monto']:,} cuota actual {info['pagadas']} de {info['total']}")
    if col2.button(f"✅ Marcar cuota pagada - {deuda}"):
        if info['pagadas'] < info['total']:
            info['pagadas'] += 1
            info['pagado'] = True
    info['pagado'] = col3.checkbox("Pagado", value=info['pagado'], key=f"{deuda}_check")

# GASTOS
st.header("📤 Gastos fijos")
total_gastos = 0
for nombre, info in datos["gastos_fijos"].items():
    col1, col2 = st.columns([4, 1])
    info["monto"] = col1.number_input(nombre, value=info["monto"], step=1000)
    info["pagado"] = col2.checkbox("Pagado", value=info["pagado"], key=f"{nombre}_check")
    total_gastos += info["monto"]

st.warning(f"💸 Total gastos fijos: ${total_gastos:,}")

# AHORRO HIJOS
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

# GUARDAR
if st.button("💾 Guardar mes"):
    guardar_datos(datos)
    st.success("✅ Datos guardados correctamente")

# HISTORIAL
st.header("📅 Ver historial")
archivos = sorted(os.listdir(DATA_DIR))
for archivo in archivos:
    if archivo.endswith(".json"):
        nombre = archivo.replace(".json", "")
        if st.button(f"📂 Ver {nombre}"):
            with open(os.path.join(DATA_DIR, archivo), "r") as f:
                data_mes = json.load(f)
            st.json(data_mes)
