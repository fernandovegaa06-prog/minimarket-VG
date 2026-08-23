import streamlit as st
import pandas as pd
from datetime import datetime
import urllib.parse

st.set_page_config(page_title="Minimarket Vega", page_icon="🛒", layout="centered")

NUMERO_WHATSAPP = "51984116361"

st.markdown("""
<style>
    .stApp {
        background: linear-gradient(-45deg, #0f766e, #115e59, #0d9488, #134e4a);
        background-size: 400% 400%;
        animation: gradientBG 15s ease infinite;
    }
    @keyframes gradientBG {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    .main-header {
        background: rgba(255, 255, 255, 0.95);
        padding: 20px;
        border-radius: 12px;
        color: #0f766e;
        margin-bottom: 20px;
    }
    h1, h2, h3, p, label { color: #ffffff !important; }
    .stDataFrame *, div[data-baseweb="select"] * { color: #1e293b !important; }
</style>
""", unsafe_allow_html=True)

if 'inventario' not in st.session_state:
    st.session_state.inventario = pd.DataFrame([
        {"Categoría": "Abarrotes", "Producto": "Arroz Costeño (kg)", "Precio Venta": 4.50, "Costo Compra": 3.80, "Stock": 25.0},
        {"Categoría": "Abarrotes", "Producto": "Azúcar Rubia (kg)", "Precio Venta": 4.00, "Costo Compra": 3.30, "Stock": 25.0},
        {"Categoría": "Abarrotes", "Producto": "Aceite Primor (1L)", "Precio Venta": 9.50, "Costo Compra": 8.20, "Stock": 25.0},
        {"Categoría": "Lácteos", "Producto": "Leche Gloria Azul (tarro)", "Precio Venta": 4.80, "Costo Compra": 4.10, "Stock": 25.0},
        {"Categoría": "Bebidas", "Producto": "Inca Kola (1.5L)", "Precio Venta": 7.50, "Costo Compra": 6.20, "Stock": 25.0},
        {"Categoría": "Bebidas", "Producto": "Agua San Luis (625ml)", "Precio Venta": 2.00, "Costo Compra": 1.30, "Stock": 25.0}
    ])

if 'ventas' not in st.session_state:
    st.session_state.ventas = []

if 'gastos' not in st.session_state:
    st.session_state.gastos = []

with st.sidebar:
    st.markdown("### 🏪 Minimarket Vega")
    st.caption("Sistema de Gestión Comercial")
    st.markdown("---")
    menu = st.selectbox(
        "Seleccione Operación:", 
        [
            "🛒 Registrar Venta", 
            "📦 Ver Stock y Montos", 
            "📊 Cierre de Caja y Balance"
        ]
    )

if menu == "🛒 Registrar Venta":
    st.markdown("""<div class="main-header"><h1>🛒 Caja y Registro de Ventas</h1><p>Control rápido de cobros, efectivo, Yape/Plin y ganancias.</p></div>""", unsafe_allow_html=True)
    lista_productos = st.session_state.inventario["Producto"].tolist()
    producto_seleccionado = st.selectbox("📦 Seleccione el producto:", lista_productos)
    prod_data = st.session_state.inventario[st.session_state.inventario["Producto"] == producto_seleccionado].iloc[0]
    stock_actual, precio_venta, costo_compra, categoria_prod = prod_data["Stock"], prod_data["Precio Venta"], prod_data["Costo Compra"], prod_data["Categoría"]
    st.info(f"📂 Categoría: **{categoria_prod}**  |  🏷️ Precio Venta: **S/ {precio_venta:.2f}**")
    cantidad = st.number_input(f"⚖️ Cantidad (Stock disponible: {stock_actual}):", min_value=0.5, max_value=float(stock_actual) if stock_actual > 0 else 1.0, value=1.0, step=0.5)
    metodo_pago = st.radio("💳 ¿Cómo pagó el cliente?", ["Efectivo", "Yape / Plin"], horizontal=True)
    total_cobrar, ganancia_estimada = cantidad * precio_venta, cantidad * (precio_venta - costo_compra)
    col_a, col_b = st.columns(2)
    with col_a: st.metric(label="💰 Total a Cobrar", value=f"S/ {total_cobrar:.2f}")
    with col_b: st.metric(label="✨ Ganancia Estimada", value=f"S/ {ganancia_estimada:.2f}")
    if st.button("✅ Cobrar y Registrar Venta", use_container_width=True):
        if stock_actual >= cantidad:
            st.session_state.inventario.loc[st.session_state.inventario["Producto"] == producto_seleccionado, "Stock"] -= cantidad
            ahora = datetime.now()
            st.session_state.ventas.append({
                "Fecha_Hora": ahora.strftime("%Y-%m-%d %H:%M"), "Fecha": ahora.strftime("%Y-%m-%d"),
                "Producto": producto_seleccionado, "Cantidad": cantidad, "Total": total_cobrar,
                "Ganancia": ganancia_estimada, "Pago": metodo_pago
            })
            st.success("🎉 ¡Venta registrada con éxito y stock descontado!")
        else:
            st.error("❌ No hay suficiente stock disponible para esta venta.")

elif menu == "📦 Ver Stock y Montos":
    st.markdown("""<div class="main-header"><h1>📦 Inventario y Valorización</h1><p>Supervisa tu mercadería en almacén valorizada en dinero.</p></div>""", unsafe_allow_html=True)
    inventario_df = st.session_state.inventario.copy()
    inventario_df["Valor Total en Stock (S/)"] = inventario_df["Stock"] * inventario_df["Precio Venta"]
    valortotal_dinero = inventario_df["Valor Total en Stock (S/)"].sum()
    col1, col2 = st.columns(2)
    with col1: st.metric(label="🏷️ Total Productos", value=len(inventario_df))
    with col2: st.metric(label="💵 Valor Total de Mercadería", value=f"S/ {valortotal_dinero:.2f}")
    st.markdown("---")
    st.dataframe(inventario_df, use_container_width=True)

elif menu == "📊 Cierre de Caja y Balance":
    st.markdown("""<div class="main-header"><h1>📊 Cierre de Caja y Balance Diario</h1><p>Resumen final de ingresos, gastos y ganancia neta.</p></div>""", unsafe_allow_html=True)
    with st.expander("💸 Registrar Gasto del Día"):
        with st.form("form_gastos"):
            desc_gasto = st.text_input("Motivo del gasto:")
            monto_gasto = st.number_input("Monto (S/):", min_value=0.0, step=0.50)
            if st.form_submit_button("Registrar Gasto") and desc_gasto:
                ahora = datetime.now()
                st.session_state.gastos.append({"Fecha": ahora.strftime("%Y-%m-%d"), "Descripción": desc_gasto, "Monto": monto_gasto})
                st.success(f"Gasto de S/ {monto_gasto:.2f} registrado.")

    fecha_hoy = datetime.now().strftime("%Y-%m-%d")
    ventas_hoy = [v for v in st.session_state.ventas if v["Fecha"] == fecha_hoy]
    gastos_hoy = [g for g in st.session_state.gastos if g["Fecha"] == fecha_hoy]

    total_ventas_hoy = sum(v["Total"] for v in ventas_hoy) if ventas_hoy else 0.0
    total_ganancia_hoy = sum(v["Ganancia"] for v in ventas_hoy) if ventas_hoy else 0.0
    total_gastos_hoy = sum(g["Monto"] for g in gastos_hoy) if gastos_hoy else 0.0
    efectivo_hoy = sum(v["Total"] for v in ventas_hoy if v["Pago"] == "Efectivo") if ventas_hoy else 0.0
    yape_hoy = sum(v["Total"] for v in ventas_hoy if v["Pago"] == "Yape / Plin") if ventas_hoy else 0.0
    ganancia_neta_hoy = total_ganancia_hoy - total_gastos_hoy

    st.subheader(f"📅 Resumen de Hoy ({fecha_hoy})")
    col1, col2, col3 = st.columns(3)
    with col1: st.metric(label="💰 Total Vendido", value=f"S/ {total_ventas_hoy:.2f}")
    with col2: st.metric(label="💵 Efec / 📱 Yape", value=f"S/ {efectivo_hoy:.1f} / S/ {yape_hoy:.1f}")
    with col3: st.metric(label="📉 Gastos", value=f"S/ {total_gastos_hoy:.2f}")
    st.success(f"🌟 **Ganancia Neta del Día:** S/ {ganancia_neta_hoy:.2f}")

    texto_wsp = f"*🏪 MINIMARKET VEGA - REPORTE DIARIO*\n📅 *Fecha:* {fecha_hoy}\n💰 *Total Vendido:* S/ {total_ventas_hoy:.2f}\n💵 *Efectivo:* S/ {efectivo_hoy:.2f}\n📱 *Yape / Plin:* S/ {yape_hoy:.2f}\n📉 *Total Gastos:* S/ {total_gastos_hoy:.2f}\n🌟 *Ganancia Neta:* S/ {ganancia_neta_hoy:.2f}\n"
    url_whatsapp = f"https://api.whatsapp.com/send?phone={NUMERO_WHATSAPP}&text={urllib.parse.quote(texto_wsp)}"
    st.markdown(f"""<a href="{url_whatsapp}" target="_blank" style="text-decoration: none;"><div style="background-color: #25d366; color: white; padding: 12px 20px; border-radius: 8px; text-align: center; font-weight: bold; font-size: 16px; margin-top: 15px;">💬 Enviar Reporte a mi WhatsApp</div></a>""", unsafe_allow_html=True)
