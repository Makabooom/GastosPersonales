
# app_gastos.py
import streamlit as st
import json
import os
from datetime import datetime

st.set_page_config(page_title="Mis Finanzas", page_icon="💸", layout="wide")
DATA_DIR = "data"
os.makedirs(DATA_DIR, exist_ok=True)

# Obtener lista de meses con datos
def obtener_meses_disponibles():
    return sorted([f.replace(".json", "") for f in os.listdir(DATA_DIR) if f.endswith(".json")])

# Selección de mes
mes_actual = datetime.now().strftime("%Y-%m")
meses = obtener_meses_disponibles()
if mes_actual not in meses:
    meses.append(mes_actual)
mes_seleccionado = st.selectbox("📅 Selecciona el mes", options=meses[::-1])
archivo_mes = os.path.join(DATA_DIR, f"{mes_seleccionado}.json")

# Cargar datos
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

        # Traer sueldo reservado del mes anterior
        anteriores = [f for f in obtener_meses_disponibles() if f < mes_seleccionado]
        if anteriores:
            mes_anterior = anteriores[-1]
            with open(os.path.join(DATA_DIR, f"{mes_anterior}.json"), "r") as f:
                datos_anteriores = json.load(f)
                sueldo_reservado = datos_anteriores.get("provisiones_mensuales", {}).get("💼 Sueldo próximo mes", {})
                if sueldo_reservado.get("provisionado"):
                    datos["ingresos_fijos"]["Sueldo AIEP"] += sueldo_reservado.get("monto", 0)
        return datos

def guardar_datos(datos):
    with open(archivo_mes, "w") as f:
        json.dump(datos, f, indent=4)

# Cargar datos
datos = cargar_datos()

# INGRESOS
st.header("📥 Ingresos")
total_ingresos = 0
for key in datos["ingresos_fijos"]:
    datos["ingresos_fijos"][key] = st.number_input(f"{key}", value=datos["ingresos_fijos"][key], min_value=0, step=1000)
    total_ingresos += datos["ingresos_fijos"][key]

st.subheader("💌 Ingresos por correos")
st.write(f"Total: ${sum(datos['ingresos_correos']):,}")
nuevo_correo = st.number_input("Agregar ingreso por correos", min_value=0, step=1000)
if st.button("➕ Agregar ingreso por correos"):
    datos["ingresos_correos"].append(nuevo_correo)
total_ingresos += sum(datos["ingresos_correos"])

st.subheader("🎁 Otros ingresos")
st.write(f"Total: ${sum(datos['ingresos_otros']):,}")
nuevo_otro = st.number_input("Agregar otro ingreso", min_value=0, step=1000)
if st.button("➕ Agregar otro ingreso"):
    datos["ingresos_otros"].append(nuevo_otro)
total_ingresos += sum(datos["ingresos_otros"])

# DEUDAS
st.header("💳 Deudas")
total_deudas = 0
for deuda, info in datos["deudas"].items():
    st.write(f"**{deuda}**: cuota actual {info['pagadas']} / {info['total']}")
    cuotas_mes = st.number_input(f"Cuotas pagadas este mes ({deuda})", min_value=0, value=info["pagadas_este_mes"], key=f"{deuda}_cuotas")
    if st.button(f"Registrar pago - {deuda}"):
        info["pagadas_este_mes"] = cuotas_mes
        info["pagadas"] += cuotas_mes
    total_deudas += info["monto"] * cuotas_mes

# GASTOS FIJOS
st.header("📤 Gastos fijos")
total_gastos = 0
for nombre, info in datos["gastos_fijos"].items():
    col1, col2 = st.columns([4, 1])
    info["monto"] = col1.number_input(nombre, value=info["monto"], step=1000, key=f"{nombre}_monto")
    info["provisionado"] = col2.checkbox("Provisionado", value=info["provisionado"], key=f"{nombre}_prov")
    total_gastos += info["monto"]

# AHORRO HIJOS
st.header("👶 Ahorro hijos")
total_ahorro = 0
for hijo, info in datos["ahorro_hijos"].items():
    st.write(f"{hijo} - ahorro auto: ${info['auto']}")
    extra = st.number_input(f"Ahorro extra {hijo}", min_value=0, step=1000, key=f"{hijo}_extra")
    if st.button(f"Agregar ahorro extra {hijo}"):
        info["extra"].append(extra)
    total_ahorro += info["auto"] + sum(info["extra"])

# PROVISIONES
st.header("🟦 Provisiones mensuales")
total_prov = 0
for nombre, info in datos["provisiones_mensuales"].items():
    col1, col2 = st.columns([4, 1])
    info["monto"] = col1.number_input(nombre, value=info["monto"], step=1000, key=f"prov_{nombre}")
    info["provisionado"] = col2.checkbox("Provisionado", value=info["provisionado"], key=f"chk_{nombre}")
    if info["provisionado"]:
        total_prov += info["monto"]

# RESUMEN
st.header("📊 Resumen")
st.write(f"**Total ingresos:** ${total_ingresos:,}")
st.write(f"**Total deudas:** ${total_deudas:,}")
st.write(f"**Total gastos fijos:** ${total_gastos:,}")
st.write(f"**Total ahorro hijos:** ${total_ahorro:,}")
st.write(f"**Total provisiones:** ${total_prov:,}")
saldo = total_ingresos - (total_deudas + total_gastos + total_ahorro + total_prov)
st.success(f"💰 Saldo estimado: ${saldo:,}")

# GUARDAR
if st.button("💾 Guardar mes"):
    guardar_datos(datos)
    st.success("✅ Mes guardado correctamente")
