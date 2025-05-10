
# app_gastos.py
import streamlit as st
import json
import os
from datetime import datetime

st.set_page_config(page_title="Mis Finanzas", page_icon="💸", layout="wide")

# Crear carpeta de datos
DATA_DIR = "data"
os.makedirs(DATA_DIR, exist_ok=True)
fecha_actual = datetime.now().strftime("%Y-%m")
archivo_mes = os.path.join(DATA_DIR, f"{fecha_actual}.json")

# Función para cargar datos
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
                "Santander": {"monto": 41128, "pagadas": 9, "total": 120, "pagado": False, "pagadas_este_mes": 0},
                "Scotiabank": {"monto": 272060, "pagadas": 9, "total": 120, "pagado": False, "pagadas_este_mes": 0},
                "Cencosud": {"monto": 163179, "pagadas": 9, "total": 120, "pagado": False, "pagadas_este_mes": 0},
                "Ripley": {"monto": 28419, "pagadas": 9, "total": 120, "pagado": False, "pagadas_este_mes": 0},
                "Falabella": {"monto": 14743, "pagadas": 9, "total": 120, "pagado": False, "pagadas_este_mes": 0}
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
                "Mercadería": {"monto": 750000, "cuenta": "Cuenta Separada", "provisionado": False}
            },
            "provisiones_mensuales": {
                "Ahorro": {"monto": 0, "provisionado": False},
                "Auto": {"monto": 30000, "provisionado": False},
                "Emergencias": {"monto": 0, "provisionado": False},
                "Pasajes": {"monto": 40000, "provisionado": False},
                "Remedios": {"monto": 70000, "provisionado": False},
                "Ropa": {"monto": 20000, "provisionado": False},
                "Mascotas": {"monto": 10000, "provisionado": False},
                "Gas": {"monto": 10000, "provisionado": False},
                "Eventos": {"monto": 0, "provisionado": False},
                "Leña": {"monto": 40000, "provisionado": False},
                "Cuotas": {"monto": 70000, "provisionado": False},
                "Arriendo": {"monto": 0, "provisionado": False}
            }
        }

def guardar_datos(data):
    with open(archivo_mes, "w") as f:
        json.dump(data, f, indent=4)

# Interfaz principal
st.title("💸 Control de Finanzas Personales")
datos = cargar_datos()

# Provisiones mensuales
st.header("🟦 Provisiones mensuales")
total_prov_esperado = 0
total_prov_real = 0
for nombre, info in datos["provisiones_mensuales"].items():
    col1, col2, col3 = st.columns([3, 2, 1])
    info["monto"] = col1.number_input(f"{nombre}", min_value=0, value=info["monto"], step=1000, key=f"prov_{nombre}")
    info["provisionado"] = col2.checkbox("✅ Provisionado", value=info["provisionado"], key=f"chk_{nombre}")
    total_prov_esperado += info["monto"]
    if info["provisionado"]:
        total_prov_real += info["monto"]
st.info(f"💼 Total esperado: ${total_prov_esperado:,} — ✅ Total provisionado: ${total_prov_real:,}")

# Guardar
if st.button("💾 Guardar mes"):
    guardar_datos(datos)
    st.success("✅ Datos guardados correctamente")
