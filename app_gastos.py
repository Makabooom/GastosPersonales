
# app_gastos.py
import streamlit as st
import json
import os
from datetime import datetime

st.set_page_config(page_title="Mis Finanzas", page_icon="💸", layout="wide")
DATA_DIR = "data"
os.makedirs(DATA_DIR, exist_ok=True)

def obtener_meses_disponibles():
    return sorted([f.replace(".json", "") for f in os.listdir(DATA_DIR) if f.endswith(".json")])

mes_actual = datetime.now().strftime("%Y-%m")
meses = obtener_meses_disponibles()
if mes_actual not in meses:
    meses.append(mes_actual)
mes_seleccionado = st.selectbox("📅 Selecciona el mes", options=meses[::-1])
archivo_mes = os.path.join(DATA_DIR, f"{mes_seleccionado}.json")

def cargar_datos():
    if os.path.exists(archivo_mes):
        with open(archivo_mes, "r") as f:
            return json.load(f)
    else:
        datos = {
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
                "Santander": {"monto": 41128, "pagadas": 9, "total": 120, "pagadas_este_mes": 0},
                "Scotiabank": {"monto": 272060, "pagadas": 9, "total": 120, "pagadas_este_mes": 0},
                "Cencosud": {"monto": 163179, "pagadas": 9, "total": 120, "pagadas_este_mes": 0},
                "Ripley": {"monto": 28419, "pagadas": 9, "total": 120, "pagadas_este_mes": 0},
                "Falabella": {"monto": 14743, "pagadas": 9, "total": 120, "pagadas_este_mes": 0}
            },
            "gastos_fijos": {
                "Arriendo": {"monto": 350000, "cuenta": "Cuenta Normal", "provisionado": False},
                "Luz": {"monto": 70000, "cuenta": "Cuenta Normal", "provisionado": False},
                "Agua": {"monto": 35000, "cuenta": "Cuenta Normal", "provisionado": False},
                "Teléfono Entel": {"monto": 210000, "cuenta": "Cuenta Normal", "provisionado": False},
                "Teléfono Wom": {"monto": 15000, "cuenta": "Cuenta Normal", "provisionado": False},
                "Internet": {"monto": 32000, "cuenta": "Tenpo", "provisionado": False},
                "Cable": {"monto": 30000, "cuenta": "Tenpo", "provisionado": False},
                "Netflix": {"monto": 13000, "cuenta": "Tenpo", "provisionado": False},
                "YouTube Premium": {"monto": 10000, "cuenta": "Tenpo", "provisionado": False},
                "Disney+": {"monto": 10000, "cuenta": "Tenpo", "provisionado": False},
                "Spotify": {"monto": 7050, "cuenta": "Tenpo", "provisionado": False},
                "ChatGPT": {"monto": 20000, "cuenta": "Tenpo", "provisionado": False},
                "Otros Play Store": {"monto": 40000, "cuenta": "Tenpo", "provisionado": False},
                "Bencina": {"monto": 150000, "cuenta": "Copec Pay", "provisionado": False},
                "Mercadería": {"monto": 670000, "cuenta": "Cuenta Separada", "provisionado": False}
            },
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

        anteriores = [f for f in obtener_meses_disponibles() if f < mes_seleccionado]
        if anteriores:
            anterior = anteriores[-1]
            with open(os.path.join(DATA_DIR, f"{anterior}.json"), "r") as f:
                datos_ant = json.load(f)
                sueldo_reservado = datos_ant.get("provisiones_mensuales", {}).get("💼 Sueldo próximo mes", {})
                if sueldo_reservado.get("provisionado"):
                    datos["ingresos_fijos"]["Sueldo AIEP"] += sueldo_reservado.get("monto", 0)
        return datos

def guardar_datos(datos):
    with open(archivo_mes, "w") as f:
        json.dump(datos, f, indent=4)

st.title("💸 Control de Finanzas Personales (Completo)")

datos = cargar_datos()

# GUARDAR botón simple para esta versión
if st.button("💾 Guardar mes"):
    guardar_datos(datos)
    st.success("✅ Datos guardados correctamente")
