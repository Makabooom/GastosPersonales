
# app_gastos.py
# App interactiva de Finanzas de Maca - versión final con tablas editables
import streamlit as st
import pandas as pd
import json
import os
from datetime import datetime

st.set_page_config(page_title="💸 Finanzas de Maca", layout="wide")
DATA_DIR = "data"
os.makedirs(DATA_DIR, exist_ok=True)

def obtener_meses():
    return sorted([f.replace(".json", "") for f in os.listdir(DATA_DIR) if f.endswith(".json")])

mes_actual = datetime.now().strftime("%Y-%m")
meses = obtener_meses()
if mes_actual not in meses:
    meses.append(mes_actual)
mes = st.selectbox("📅 Selecciona el mes", options=meses[::-1])
archivo_mes = os.path.join(DATA_DIR, f"{mes}.json")

# Datos base
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
            "Santander": [41128, 120, 9, 0],
            "Scotiabank": [272060, 120, 9, 0],
            "Cencosud": [163179, 120, 9, 0],
            "Ripley": [28419, 120, 9, 0],
            "Falabella": [14743, 120, 9, 0]
        },
        "gastos": {
            "Arriendo": [350000, "Cuenta Normal", False, False],
            "Luz": [70000, "Cuenta Normal", False, False],
            "Agua": [35000, "Cuenta Normal", False, False],
            "Teléfono Entel": [210000, "Cuenta Normal", False, False],
            "Teléfono Wom": [15000, "Cuenta Normal", False, False],
            "Internet": [32000, "Tenpo", False, False],
            "Cable": [30000, "Tenpo", False, False],
            "Netflix": [13000, "Tenpo", False, False],
            "YouTube Premium": [10000, "Tenpo", False, False],
            "Disney+": [10000, "Tenpo", False, False],
            "Spotify": [7050, "Tenpo", False, False],
            "ChatGPT": [20000, "Tenpo", False, False],
            "Otros Play Store": [40000, "Tenpo", False, False],
            "Bencina": [150000, "Copec Pay", False, False],
            "Mercadería": [670000, "Cuenta Separada", False, False]
        },
        "ahorros": {
            "Sebastián": [5000, []],
            "Hernán": [5000, []],
            "Mailen": [5000, []]
        },
        "provisiones": {
            "Ahorro": [0, False, 0, "No programado"],
            "Auto": [30000, False, 0, "Reparaciones"],
            "Emergencias": [0, False, 0, "No programado"],
            "Pasajes": [20000, False, 0, "Viajes a Santiago"],
            "Remedios": [100000, False, 0, "Medicamentos niños"],
            "Ropa": [20000, False, 0, "Ahorro progresivo"],
            "Mascotas": [10000, False, 0, "Veterinario y comida"],
            "Gas": [10000, False, 0, "Calefacción"],
            "Eventos": [0, False, 0, "Cumpleaños, celebraciones"],
            "Leña": [40000, False, 0, "Compra anual"],
            "Cuotas escolares/talleres": [30000, False, 0, "Escolaridad"],
            "Arriendo (quincenal)": [0, False, 0, "Pago en dos partes"],
            "💼 Sueldo próximo mes": [0, False, 0, "Reserva para próximo mes"]
        }
    }

# Cargar datos
def cargar_datos():
    if os.path.exists(archivo_mes):
        with open(archivo_mes, "r") as f:
            return json.load(f)
    else:
        datos = datos_base()
        prev = [m for m in obtener_meses() if m < mes]
        if prev:
            ant = prev[-1]
            with open(os.path.join(DATA_DIR, f"{ant}.json")) as f:
                ant_data = json.load(f)
                sueldo = ant_data["provisiones"]["💼 Sueldo próximo mes"]
                if sueldo[1]:
                    datos["ingresos"]["Ingreso provisionado"] = sueldo[0]
        return datos

def guardar_datos(datos):
    with open(archivo_mes, "w") as f:
        json.dump(datos, f, indent=2)

datos = cargar_datos()

# --- Ingresos ---
st.header("📥 Ingresos")
df_ing = pd.DataFrame([
    ["Ingreso provisionado", datos["ingresos"]["Ingreso provisionado"]],
    ["Sueldo", datos["ingresos"]["Sueldo"]],
    ["Pensión hijo", datos["ingresos"]["Pensión hijo"]]
], columns=["Tipo", "Monto"])
df_ing = st.data_editor(df_ing, num_rows="dynamic", use_container_width=True)
datos["ingresos"]["Ingreso provisionado"] = df_ing.loc[df_ing["Tipo"] == "Ingreso provisionado", "Monto"].values[0]
datos["ingresos"]["Sueldo"] = df_ing.loc[df_ing["Tipo"] == "Sueldo", "Monto"].values[0]
datos["ingresos"]["Pensión hijo"] = df_ing.loc[df_ing["Tipo"] == "Pensión hijo", "Monto"].values[0]

st.subheader("➕ Ingresos por correos y otros")
nuevo_correo = st.number_input("Agregar ingreso por correos", 0, step=1000)
if st.button("Agregar correo"):
    datos["ingresos"]["Correos"].append(nuevo_correo)
nuevo_otro = st.number_input("Agregar otro ingreso", 0, step=1000)
if st.button("Agregar otro"):
    datos["ingresos"]["Otros"].append(nuevo_otro)

# --- Deudas ---
st.header("💳 Deudas")
df_deuda = pd.DataFrame([
    [k] + v for k, v in datos["deudas"].items()
], columns=["Entidad", "Monto cuota", "Total cuotas", "Pagadas", "Pagadas este mes"])
df_deuda = st.data_editor(df_deuda, num_rows="fixed", use_container_width=True)
for i, row in df_deuda.iterrows():
    datos["deudas"][row["Entidad"]] = [row["Monto cuota"], row["Total cuotas"], row["Pagadas"], row["Pagadas este mes"]]

# --- Gastos fijos ---
st.header("📤 Gastos fijos")
df_gastos = pd.DataFrame([
    [k] + v for k, v in datos["gastos"].items()
], columns=["Gasto", "Monto", "Cuenta", "Provisionado", "Efectuado"])
df_gastos = st.data_editor(df_gastos, num_rows="fixed", use_container_width=True)
for i, row in df_gastos.iterrows():
    datos["gastos"][row["Gasto"]] = [row["Monto"], row["Cuenta"], row["Provisionado"], row["Efectuado"]]

# --- Ahorros hijos ---
st.header("👶 Ahorros por hijo")
df_ahorro = pd.DataFrame([
    [k, v[0], sum(v[1])] for k, v in datos["ahorros"].items()
], columns=["Hijo", "Ahorro automático", "Extra acumulado"])
st.table(df_ahorro)
for hijo in datos["ahorros"]:
    extra = st.number_input(f"Ahorro extra para {hijo}", 0, step=1000, key=f"extra_{hijo}")
    if st.button(f"Agregar ahorro extra - {hijo}"):
        datos["ahorros"][hijo][1].append(extra)

# --- Provisiones ---
st.header("🟦 Provisiones")
df_prov = pd.DataFrame([
    [k] + v for k, v in datos["provisiones"].items()
], columns=["Ítem", "Monto objetivo", "Provisionado", "Gasto real", "Comentario"])
df_prov = st.data_editor(df_prov, num_rows="fixed", use_container_width=True)
for i, row in df_prov.iterrows():
    datos["provisiones"][row["Ítem"]] = [row["Monto objetivo"], row["Provisionado"], row["Gasto real"], row["Comentario"]]

# --- Resumen ---
st.header("📊 Resumen")
total_ingresos = datos["ingresos"]["Ingreso provisionado"] + datos["ingresos"]["Sueldo"] + datos["ingresos"]["Pensión hijo"] + sum(datos["ingresos"]["Correos"]) + sum(datos["ingresos"]["Otros"])
total_deudas = sum(v[0]*v[3] for v in datos["deudas"].values())
total_gastos = sum(v[0] for v in datos["gastos"].values() if v[3])  # Solo si efectuado
total_ahorro = sum(v[0] + sum(v[1]) for v in datos["ahorros"].values())
total_prov = sum(v[0] for v in datos["provisiones"].values() if v[1])
total_gastado_prov = sum(v[2] for v in datos["provisiones"].values())

saldo = total_ingresos - (total_deudas + total_gastos + total_ahorro + total_prov)

st.write(f"**Total ingresos:** ${total_ingresos:,}")
st.write(f"**Total deudas pagadas:** ${total_deudas:,}")
st.write(f"**Total gastos efectuados:** ${total_gastos:,}")
st.write(f"**Total ahorro hijos:** ${total_ahorro:,}")
st.write(f"**Total provisiones hechas:** ${total_prov:,}")
st.write(f"**Gasto real desde provisiones:** ${total_gastado_prov:,}")
st.success(f"💰 **Saldo estimado del mes:** ${saldo:,}")

if st.button("💾 Guardar mes"):
    guardar_datos(datos)
    st.success("✅ Datos guardados correctamente.")
