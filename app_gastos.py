
# app_gastos.py
import streamlit as st
import json
import os
from datetime import datetime

st.set_page_config(page_title="Mis Finanzas", page_icon="💸", layout="wide")

# Crear carpeta para guardar datos mensuales
DATA_DIR = "data"
os.makedirs(DATA_DIR, exist_ok=True)

# Archivo del mes actual
fecha_actual = datetime.now().strftime("%Y-%m")
archivo_mes = os.path.join(DATA_DIR, f"{fecha_actual}.json")

# Cargar datos
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
            "provisiones": [
                {"nombre": "Leña", "monto": 20000, "cuenta": "Cuenta Normal", "provisionado": False}
            ]
        }

def guardar_datos(data):
    with open(archivo_mes, "w") as f:
        json.dump(data, f, indent=4)

# Interfaz
st.title("💸 Control de Finanzas Personales")
datos = cargar_datos()

# INGRESOS
st.header("📥 Ingresos")
for key in datos["ingresos_fijos"]:
    datos["ingresos_fijos"][key] = st.number_input(f"{key}", min_value=0, value=datos["ingresos_fijos"][key], step=1000)

st.subheader("💌 Ingresos por correos")
st.write(f"Total: ${sum(datos['ingresos_correos']):,}")
nuevo_correo = st.number_input("Agregar ingreso por correos", min_value=0, step=1000)
if st.button("➕ Agregar ingreso por correos"):
    datos["ingresos_correos"].append(nuevo_correo)

st.subheader("🎁 Otros ingresos")
st.write(f"Total: ${sum(datos['ingresos_otros']):,}")
nuevo_otro = st.number_input("Agregar otro ingreso", min_value=0, step=1000)
if st.button("➕ Agregar otro ingreso"):
    datos["ingresos_otros"].append(nuevo_otro)

# DEUDAS
st.header("💳 Deudas")
for deuda, info in datos["deudas"].items():
    st.write(f"**{deuda}** - cuota actual: {info['pagadas']} / {info['total']}")
    cuotas_mes = st.number_input(f"Cuotas pagadas este mes ({deuda})", min_value=0, value=info["pagadas_este_mes"], step=1, key=f"{deuda}_cuotas")
    if st.button(f"Registrar cuotas pagadas de {deuda}"):
        info["pagadas_este_mes"] = cuotas_mes
        info["pagadas"] += cuotas_mes
        info["pagado"] = True
    info["pagado"] = st.checkbox(f"{deuda} pagado este mes", value=info["pagado"], key=f"{deuda}_check")

# GASTOS FIJOS
st.header("📤 Gastos fijos")
for nombre, info in datos["gastos_fijos"].items():
    st.write(f"**{nombre}** ({info['cuenta']})")
    info["monto"] = st.number_input(f"Monto: {nombre}", min_value=0, value=info["monto"], step=1000, key=f"{nombre}_monto")
    info["provisionado"] = st.checkbox(f"Provisionado ({nombre})", value=info["provisionado"], key=f"{nombre}_prov")

# AHORRO HIJOS
st.header("👶 Ahorros para los hijos")
for hijo, info in datos["ahorro_hijos"].items():
    st.write(f"**{hijo}** - Ahorro automático: ${info['auto']}")
    extra = st.number_input(f"Ahorro extra para {hijo}", min_value=0, step=1000, key=f"{hijo}_extra")
    if st.button(f"➕ Agregar ahorro extra - {hijo}"):
        info["extra"].append(extra)

# PROVISIONES
st.header("📂 Provisiones especiales (no mensuales)")
for i, p in enumerate(datos["provisiones"]):
    st.write(f"**{p['nombre']}** - ${p['monto']} ({p['cuenta']})")
    p["provisionado"] = st.checkbox(f"{p['nombre']} provisionado", value=p["provisionado"], key=f"prov_{i}")

# Guardar
if st.button("💾 Guardar mes"):
    guardar_datos(datos)
    st.success("✅ Datos guardados correctamente")
