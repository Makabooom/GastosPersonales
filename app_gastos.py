
# app_gastos.py
# --- Resumen completo: Finanzas de Maca ---
import streamlit as st
import json
import os
from datetime import datetime

st.set_page_config(page_title="💸 Mis Finanzas", layout="wide")
DATA_DIR = "data"
os.makedirs(DATA_DIR, exist_ok=True)

# Obtener y seleccionar mes
def obtener_meses():
    return sorted([f.replace(".json", "") for f in os.listdir(DATA_DIR) if f.endswith(".json")])

mes_actual = datetime.now().strftime("%Y-%m")
meses = obtener_meses()
if mes_actual not in meses:
    meses.append(mes_actual)
mes = st.selectbox("📅 Selecciona el mes", options=meses[::-1])
archivo_mes = os.path.join(DATA_DIR, f"{mes}.json")

# Datos iniciales base
def datos_base():
    return {
        "ingresos": {
            "Ingreso provisionado": 0,
            "Sueldo": 0,
            "Pensión hijo": 0,
            "Correos": [],
            "Otros": []
        },
        "deudas": {
            "Santander": {"cuota": 41128, "total": 120, "pagadas": 9, "mes": 0},
            "Scotiabank": {"cuota": 272060, "total": 120, "pagadas": 9, "mes": 0},
            "Cencosud": {"cuota": 163179, "total": 120, "pagadas": 9, "mes": 0},
            "Ripley": {"cuota": 28419, "total": 120, "pagadas": 9, "mes": 0},
            "Falabella": {"cuota": 14743, "total": 120, "pagadas": 9, "mes": 0}
        },
        "gastos": {
            "Arriendo": [350000, "Cuenta Normal", False],
            "Luz": [70000, "Cuenta Normal", False],
            "Agua": [35000, "Cuenta Normal", False],
            "Teléfono Entel": [210000, "Cuenta Normal", False],
            "Teléfono Wom": [15000, "Cuenta Normal", False],
            "Internet": [32000, "Tenpo", False],
            "Cable": [30000, "Tenpo", False],
            "Netflix": [13000, "Tenpo", False],
            "YouTube Premium": [10000, "Tenpo", False],
            "Disney+": [10000, "Tenpo", False],
            "Spotify": [7050, "Tenpo", False],
            "ChatGPT": [20000, "Tenpo", False],
            "Otros Play Store": [40000, "Tenpo", False],
            "Bencina": [150000, "Copec Pay", False],
            "Mercadería": [670000, "Cuenta Separada", False]
        },
        "ahorros": {
            "Sebastián": {"auto": 5000, "extra": []},
            "Hernán": {"auto": 5000, "extra": []},
            "Mailen": {"auto": 5000, "extra": []}
        },
        "provisiones": {
            "Ahorro": [0, False, "No programado"],
            "Auto": [30000, False, "Reparaciones y mantenciones"],
            "Emergencias": [0, False, "No programado"],
            "Pasajes": [20000, False, "Para viajes a Santiago"],
            "Remedios": [100000, False, "Medicamentos para los niños"],
            "Ropa": [20000, False, "Ahorro progresivo"],
            "Mascotas": [10000, False, "Veterinario y comida"],
            "Gas": [10000, False, "Balones, calefacción"],
            "Eventos": [0, False, "Cumpleaños y celebraciones"],
            "Leña": [40000, False, "Compra anual"],
            "Cuotas escolares/talleres": [30000, False, "Escolaridad y actividades"],
            "Arriendo (quincenal)": [0, False, "Si decides dividir el pago"],
            "💼 Sueldo próximo mes": [0, False, "Se carga como ingreso en el mes siguiente"]
        }
    }

# Cargar datos del mes
def cargar_datos():
    if os.path.exists(archivo_mes):
        with open(archivo_mes, "r") as f:
            return json.load(f)
    else:
        datos = datos_base()
        # Traer ingreso provisionado del mes anterior
        anteriores = [m for m in obtener_meses() if m < mes]
        if anteriores:
            ant = anteriores[-1]
            with open(os.path.join(DATA_DIR, f"{ant}.json")) as f:
                d_ant = json.load(f)
                sueldo = d_ant["provisiones"].get("💼 Sueldo próximo mes", [0, False])[0]
                marcado = d_ant["provisiones"].get("💼 Sueldo próximo mes", [0, False])[1]
                if marcado:
                    datos["ingresos"]["Ingreso provisionado"] = sueldo
        return datos

def guardar_datos(datos):
    with open(archivo_mes, "w") as f:
        json.dump(datos, f, indent=2)

datos = cargar_datos()

# INGRESOS
st.header("📥 Ingresos")
datos["ingresos"]["Sueldo"] = st.number_input("Sueldo", value=datos["ingresos"]["Sueldo"], step=1000)
datos["ingresos"]["Pensión hijo"] = st.number_input("Pensión hijo", value=datos["ingresos"]["Pensión hijo"], step=1000)
st.write(f"💼 Ingreso provisionado desde el mes anterior: **${datos['ingresos']['Ingreso provisionado']:,}**")
nuevo_correo = st.number_input("➕ Ingreso por correos", 0, step=1000)
if st.button("Agregar ingreso correo"):
    datos["ingresos"]["Correos"].append(nuevo_correo)
nuevo_otro = st.number_input("➕ Otro ingreso", 0, step=1000)
if st.button("Agregar otro ingreso"):
    datos["ingresos"]["Otros"].append(nuevo_otro)

# DEUDAS
st.header("💳 Deudas")
total_deuda = 0
st.markdown("| Entidad | Cuota | Total | Pagadas | Este mes |")
for ent, val in datos["deudas"].items():
    col1, col2 = st.columns([3, 2])
    val["mes"] = col2.number_input(f"{ent} cuotas este mes", 0, 12, val["mes"], key=f"{ent}_cuotas")
    if st.button(f"Registrar pago {ent}"):
        val["pagadas"] += val["mes"]
        total_deuda += val["cuota"] * val["mes"]

# GASTOS
st.header("📤 Gastos fijos")
total_gastos = 0
for nombre, (monto, cuenta, prov) in datos["gastos"].items():
    col1, col2, col3 = st.columns([3, 2, 2])
    monto = col1.number_input(f"{nombre}", value=monto, step=1000, key=f"{nombre}_monto")
    prov = col3.checkbox("Provisionado", value=prov, key=f"{nombre}_prov")
    datos["gastos"][nombre] = [monto, cuenta, prov]
    if prov:
        total_gastos += monto
    col2.write(f"Cuenta: {cuenta}")

# AHORROS
st.header("👶 Ahorro por hijo")
total_ahorro = 0
for hijo, info in datos["ahorros"].items():
    st.write(f"**{hijo}** (auto: ${info['auto']})")
    extra = st.number_input(f"Ahorro extra para {hijo}", min_value=0, step=1000, key=f"extra_{hijo}")
    if st.button(f"Agregar ahorro extra - {hijo}"):
        info["extra"].append(extra)
    total_ahorro += info["auto"] + sum(info["extra"])

# PROVISIONES
st.header("🟦 Provisiones mensuales")
total_prov = 0
for nombre, (monto, marcado, comentario) in datos["provisiones"].items():
    col1, col2 = st.columns([4, 2])
    monto = col1.number_input(f"{nombre}", value=monto, step=1000, key=f"prov_{nombre}")
    marcado = col2.checkbox(f"✅ Provisionado", value=marcado, key=f"chk_{nombre}")
    datos["provisiones"][nombre] = [monto, marcado, comentario]
    if marcado:
        total_prov += monto
    if comentario:
        st.caption(f"💬 {comentario}")

# RESUMEN FINAL
st.header("📊 Resumen mensual")
total_ing = datos["ingresos"]["Ingreso provisionado"] + datos["ingresos"]["Sueldo"] + datos["ingresos"]["Pensión hijo"] + sum(datos["ingresos"]["Correos"]) + sum(datos["ingresos"]["Otros"])
st.write(f"**Total ingresos:** ${total_ing:,}")
st.write(f"**Total deudas pagadas este mes:** ${total_deuda:,}")
st.write(f"**Total gastos fijos (provisionados):** ${total_gastos:,}")
st.write(f"**Total ahorro hijos:** ${total_ahorro:,}")
st.write(f"**Total provisiones:** ${total_prov:,}")
saldo = total_ing - (total_deuda + total_gastos + total_ahorro + total_prov)
st.success(f"💰 **Saldo estimado del mes:** ${saldo:,}")

if st.button("💾 Guardar mes"):
    guardar_datos(datos)
    st.success("✅ Datos guardados correctamente.")
