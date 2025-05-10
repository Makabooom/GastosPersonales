
# app_gastos.py
import streamlit as st
import json
import os
from datetime import datetime

st.set_page_config(page_title="💸 Mis Finanzas", layout="wide")
DATA_DIR = "data"
os.makedirs(DATA_DIR, exist_ok=True)

# Obtener lista de meses con datos
def obtener_meses_disponibles():
    return sorted([f.replace(".json", "") for f in os.listdir(DATA_DIR) if f.endswith(".json")])

# Selección de mes
meses = obtener_meses_disponibles()
mes_actual = datetime.now().strftime("%Y-%m")
mes_seleccionado = st.selectbox("📅 Selecciona el mes", options=[mes_actual] + meses[::-1])

archivo_mes = os.path.join(DATA_DIR, f"{mes_seleccionado}.json")

# Cargar datos del mes
def cargar_datos():
    if os.path.exists(archivo_mes):
        with open(archivo_mes, "r") as f:
            datos = json.load(f)
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
                "Santander": {"monto": 41128, "pagadas": 9, "total": 120, "pagado": False, "pagadas_este_mes": 0},
                "Scotiabank": {"monto": 272060, "pagadas": 9, "total": 120, "pagado": False, "pagadas_este_mes": 0},
                "Cencosud": {"monto": 163179, "pagadas": 9, "total": 120, "pagado": False, "pagadas_este_mes": 0},
                "Ripley": {"monto": 28419, "pagadas": 9, "total": 120, "pagado": False, "pagadas_este_mes": 0},
                "Falabella": {"monto": 14743, "pagadas": 9, "total": 120, "pagado": False, "pagadas_este_mes": 0}
            },
            "gastos_fijos": {
                "Mercadería": {"monto": 670000, "cuenta": "Cuenta Separada", "provisionado": False}
            },
            "provisiones_mensuales": {
                "💼 Sueldo próximo mes": {"monto": 0, "provisionado": False}
            }
        }

        # Si es un nuevo mes, importar sueldo reservado del mes anterior
        meses_anteriores = [f for f in obtener_meses_disponibles() if f < mes_seleccionado]
        if meses_anteriores:
            ultimo_mes = meses_anteriores[-1]
            with open(os.path.join(DATA_DIR, f"{ultimo_mes}.json"), "r") as f:
                anterior = json.load(f)
                sueldo_guardado = anterior.get("provisiones_mensuales", {}).get("💼 Sueldo próximo mes", {})
                if sueldo_guardado.get("provisionado"):
                    datos["ingresos_fijos"]["Sueldo AIEP"] += sueldo_guardado.get("monto", 0)

    return datos

def guardar_datos(data):
    with open(archivo_mes, "w") as f:
        json.dump(data, f, indent=4)

# Cargar datos
datos = cargar_datos()

# Mostrar provisión de sueldo próximo mes
st.title(f"💼 Provisión de Sueldo en {mes_seleccionado}")
col1, col2 = st.columns([4, 1])
datos["provisiones_mensuales"]["💼 Sueldo próximo mes"]["monto"] = col1.number_input(
    "Monto a provisionar", min_value=0, value=datos["provisiones_mensuales"]["💼 Sueldo próximo mes"]["monto"], step=1000
)
datos["provisiones_mensuales"]["💼 Sueldo próximo mes"]["provisionado"] = col2.checkbox(
    "✅ Provisionado", value=datos["provisiones_mensuales"]["💼 Sueldo próximo mes"]["provisionado"]
)

# Guardar
if st.button("💾 Guardar cambios del mes"):
    guardar_datos(datos)
    st.success("✅ Datos del mes guardados correctamente")
