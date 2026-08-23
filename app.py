import streamlit as st
import pandas as pd
from datetime import datetime
import pytz
import urllib.parse

# Configuración de la página
st.set_page_config(page_title="Minimarket Vega", page_icon="🛒", layout="centered")

# --- CONFIGURACIÓN DE WHATSAPP Y ZONA HORARIA ---
NUMERO_WHATSAPP = "51984116361"
ZONA_PERU = pytz.timezone("America/Lima")

def obtener_tiempo_peru():
    return datetime.now(ZONA_PERU)

# --- ESTILOS VISUALES: FONDO ANIMADO Y TARJETAS MODERNAS (CSS) ---
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
        backdrop-filter: blur(10px);
        padding: 20px 25px;
        border-radius: 12px;
        color: #0f766e;
        margin-bottom: 20px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.2);
        border: 1px solid rgba(255, 255, 255, 0.18);
    }
    .main-header h1 {
        margin: 0;
        font-size: 26px;
        font-weight: 700;
        color: #0f766e;
    }
    .main-header p {
        margin: 5px 0 0 0;
        font-size: 14px;
        color: #334155;
    }

    .report-box {
        background-color: rgba(255, 255, 255, 0.95);
        border: 2px dashed #0d9488;
        padding: 20px;
        border-radius: 10px;
        margin-top: 15px;
        margin-bottom: 15px;
        color: #1e293b;
    }
    
    .stMarkdown, .stText, h1, h2, h3, p, label {
        color: #ffffff !important;
    }
    
    .report-box *, .stDataFrame *, div[data-baseweb="select"] * {
        color: #1e293b !important;
    }
</style>
""", unsafe_allow_html=True)

# --- SISTEMA DE CONTRASEÑA ---
if 'autenticado' not in st.session_state:
    st.session_state.autenticado = False

def verificar_password():
    password_ingresada = st.text_input("Contraseña de acceso:", type="password")
    if st.button("Ingresar al Sistema"):
        if password_ingresada == "1234":
            st.session_state.autenticado = True
            st.rerun()
        else:
            st.error("Contraseña incorrecta. Inténtalo de nuevo.")

if not st.session_state.autenticado:
    st.markdown("""
        <div style="text-align: center; padding: 30px; background: rgba(255, 255, 255, 0.9); border-radius: 15px; box-shadow: 0 8px 32px rgba(0,0,0,0.2);">
            <h2 style="color: #0f766e !important;">🔐 Acceso Restringido</h2>
            <p style="color: #475569 !important;">Minimarket Vega - Control de Inventario y Caja</p>
        </div>
    """, unsafe_allow_html=True)
    verificar_password()
    st.stop()

# --- BASE DE DATOS INICIAL ---
if 'inventario' not in st.session_state:
    st.session_state.inventario = pd.DataFrame([
        {"Categoría": "Abarrotes", "Producto": "Arroz Costeño (kg)", "Precio Venta": 4.50, "Costo Compra": 3.80, "Stock": 25.0},
        {"Categoría": "Abarrotes", "Producto": "Azúcar Rubia (kg)", "Precio Venta": 4.00, "Costo Compra": 3.30, "Stock": 25.0},
        {"Categoría": "Abarrotes", "Producto": "Fideos Don Vittorio (500g)", "Precio Venta": 3.20, "Costo Compra": 2.60, "Stock": 25.0},
        {"Categoría": "Abarrotes", "Producto": "Aceite Primor (1L)", "Precio Venta": 9.50, "Costo Compra": 8.20, "Stock": 25.0},
        {"Categoría": "Abarrotes", "Producto": "Atún Florida (latas)", "Precio Venta": 5.50, "Costo Compra": 4.60, "Stock": 25.0},
        {"Categoría": "Lácteos", "Producto": "Leche Gloria Azul (tarro)", "Precio Venta": 4.80, "Costo Compra": 4.10, "Stock": 25.0},
        {"Categoría": "Lácteos", "Producto": "Queso Fresco (kg)", "Precio Venta": 22.00, "Costo Compra": 18.00, "Stock": 25.0},
        {"Categoría": "Lácteos", "Producto": "Yogurt Gloria (1L)", "Precio Venta": 7.50, "Costo Compra": 6.20, "Stock": 25.0},
        {"Categoría": "Bebidas", "Producto": "Inca Kola (1.5L)", "Precio Venta": 7.50, "Costo Compra": 6.20, "Stock": 25.0},
        {"Categoría": "Bebidas", "Producto": "Coca Cola (1.5L)", "Precio Venta": 7.50, "Costo Compra": 6.20, "Stock": 25.0},
        {"Categoría": "Bebidas", "Producto": "Agua San Luis (625ml)", "Precio Venta": 2.00, "Costo Compra": 1.30, "Stock": 25.0},
        {"Categoría": "Bebidas", "Producto": "Cerveza Pilsen (Botella 650ml)", "Precio Venta": 8.50, "Costo Compra": 7.20, "Stock": 25.0},
        {"Categoría": "Golosinas", "Producto": "Galletas Sublime", "Precio Venta": 1.50, "Costo Compra": 1.10, "Stock": 25.0},
        {"Categoría": "Golosinas", "Producto": "Papas Lays (Grande)", "Precio Venta": 7.00, "Costo Compra": 5.50, "Stock": 25.0},
        {"Categoría": "Limpieza", "Producto": "Detergente Bolívar (1kg)", "Precio Venta": 11.50, "Costo Compra": 9.80, "Stock": 25.0},
        {"Categoría": "Limpieza", "Producto": "Lejía Clorox (1L)", "Precio Venta": 5.00, "Costo Compra": 3.90, "Stock": 25.0}
    ])

if 'ventas' not in st.session_state:
    st.session_state.ventas = []

if 'gastos' not in st.session_state:
    st.session_state.gastos = []

# --- MENÚ EN LA BARRA LATERAL ---
with st.sidebar:
    st.markdown("### 🏪 Minimarket Vega")
    st.caption("Sistema de Gestión Comercial")
    if st.button("🔒 Cerrar Sesión", use_container_width=True):
        st.session_state.autenticado = False
        st.rerun()
    st.markdown("---")
    menu = st.selectbox(
        "Seleccione Operación:", 
        [
            "🛒 Registrar Venta", 
            "📦 Ver Stock y Montos", 
            "🛠️ Corregir Stock / Precios",
            "📊 Cierre de Caja y Balance",
            "📅 Reporte Semanal y Mensual"
        ]
    )

# ==========================================
# OPCIÓN 1: REGISTRAR VENTA
# ==========================================
if menu == "🛒 Registrar Venta":
    st.markdown("""
        <div class="main-header">
            <h1>🛒 Caja y Registro de Ventas</h1>
            <p>Control rápido de cobros, efectivo, Yape/Plin y ganancias del día.</p>
        </div>
    """, unsafe_allow_html=True)

    lista_productos = st.session_state.inventario["Producto"].tolist()
    producto_seleccionado = st.selectbox("📦 Seleccione el producto:", lista_productos)

    prod_data = st.session_state.inventario[st.session_state.inventario["Producto"] == producto_seleccionado].iloc[0]
    stock_actual = prod_data["Stock"]
    precio_venta = prod_data["Precio Venta"]
    costo_compra = prod_data["Costo Compra"]
    categoria_prod = prod_data["Categoría"]

    st.info(f"📂 Categoría: **{categoria_prod}**  |  🏷️ Precio Venta: **S/ {precio_venta:.2f}**")

    cantidad = st.number_input(f"⚖️ Cantidad (Stock disponible: {stock_actual}):", min_value=0.5, max_value=float(stock_actual) if stock_actual > 0 else 1.0, value=1.0, step=0.5)

    st.write("💳 **¿Cómo pagó el cliente?**")
    metodo_pago = st.radio("", ["Efectivo", "Yape / Plin"], horizontal=True)

    total_cobrar = cantidad * precio_venta
    ganancia_estimada = cantidad * (precio_venta - costo_compra)

    col_a, col_b = st.columns(2)
    with col_a:
        st.metric(label="💰 Total a Cobrar", value=f"S/ {total_cobrar:.2f}")
    with col_b:
        st.metric(label="✨ Ganancia Estimada", value=f"S/ {ganancia_estimada:.2f}")

    if st.button("✅ Cobrar y Registrar Venta", use_container_width=True):
        if stock_actual >= cantidad:
            st.session_state.inventario.loc[st.session_state.inventario["Producto"] == producto_seleccionado, "Stock"] -= cantidad
            
            ahora = obtener_tiempo_peru()
            nueva_venta = {
                "Fecha_Hora": ahora.strftime("%Y-%m-%d %H:%M"),
                "Fecha": ahora.strftime("%Y-%m-%d"),
                "Producto": producto_seleccionado,
                "Cantidad": cantidad,
                "Total": total_cobrar,
                "Ganancia": ganancia_estimada,
                "Pago": metodo_pago
            }
            st.session_state.ventas.append(nueva_venta)
            st.success("🎉 ¡Venta registrada con éxito y stock descontado!")
        else:
            st.error("❌ No hay suficiente stock disponible para esta venta.")

# ==========================================
# OPCIÓN 2: VER STOCK Y MONTOS
# ==========================================
elif menu == "📦 Ver Stock y Montos":
    st.markdown("""
        <div class="main-header">
            <h1>📦 Inventario y Valorización</h1>
            <p>Supervisa tu mercadería en almacén valorizada en dinero y organizada por categorías.</p>
        </div>
    """, unsafe_allow_html=True)

    inventario_df = st.session_state.inventario.copy()
    inventario_df["Valor Total en Stock (S/)"] = inventario_df["Stock"] * inventario_df["Precio Venta"]
    valortotal_dinero = inventario_df["Valor Total en Stock (S/)"].sum()

    col1, col2 = st.columns(2)
    with col1:
        st.metric(label="🏷️ Total Productos", value=len(inventario_df))
    with col2:
        st.metric(label="💵 Valor Total de Mercadería", value=f"S/ {valortotal_dinero:.2f}")

    st.markdown("---")

    categorias_disponibles = ["Todas"] + list(inventario_df["Categoría"].unique())
    cat_elegida = st.selectbox("📂 Filtrar Inventario por Categoría:", categorias_disponibles)

    if cat_elegida != "Todas":
        inventario_filtrado = inventario_df[inventario_df["Categoría"] == cat_elegida]
    else:
        inventario_filtrado = inventario_df

    st.dataframe(inventario_filtrado, use_container_width=True)

    csv_inventario = inventario_filtrado.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Descargar Reporte de Inventario (CSV)",
        data=csv_inventario,
        file_name=f"inventario_minimarket_vega_{obtener_tiempo_peru().strftime('%Y-%m-%d')}.csv",
        mime="text/csv",
        use_container_width=True
    )

# ==========================================
# OPCIÓN 3: CORREGIR STOCK O PRECIOS
# ==========================================
elif menu == "🛠️ Corregir Stock / Precios":
    st.markdown("""
        <div class="main-header">
            <h1>🛠️ Corrección de Inventario</h1>
            <p>Actualiza precios, costos o ajusta el stock si llegó nueva mercadería.</p>
        </div>
    """, unsafe_allow_html=True)

    lista_productos_corr = st.session_state.inventario["Producto"].tolist()
    prod_a_editar = st.selectbox("🔍 Selecciona el producto a corregir:", lista_productos_corr)

    fila_prod = st.session_state.inventario[st.session_state.inventario["Producto"] == prod_a_editar].iloc[0]
    stock_viejo = fila_prod["Stock"]
    precio_viejo = fila_prod["Precio Venta"]
    costo_viejo = fila_prod["Costo Compra"]

    st.info(f"📌 Estado actual de **{prod_a_editar}** ➔ Stock: {stock_viejo} | Precio Venta: S/ {precio_viejo:.2f}")

    nuevo_stock = st.number_input("📦 Stock exacto:", value=float(stock_viejo), step=1.0)
    nuevo_precio = st.number_input("🏷️ Precio de Venta (S/):", value=float(precio_viejo), step=0.10)
    nuevo_costo = st.number_input("📉 Costo de Compra (S/):", value=float(costo_viejo), step=0.10)

    if st.button("💾 Guardar Cambios", use_container_width=True):
        st.session_state.inventario.loc[st.session_state.inventario["Producto"] == prod_a_editar, "Stock"] = nuevo_stock
        st.session_state.inventario.loc[st.session_state.inventario["Producto"] == prod_a_editar, "Precio Venta"] = nuevo_precio
        st.session_state.inventario.loc[st.session_state.inventario["Producto"] == prod_a_editar, "Costo Compra"] = nuevo_costo
        st.success(f"✅ ¡Los datos de '{prod_a_editar}' han sido actualizados con éxito!")

# ==========================================
# OPCIÓN 4: CIERRE DE CAJA Y BALANCE DEL DÍA
# ==========================================
elif menu == "📊 Cierre de Caja y Balance":
    st.markdown("""
        <div class="main-header">
            <h1>📊 Cierre de Caja y Balance Diario</h1>
            <p>Resumen final de ingresos, gastos y ganancia neta de la jornada.</p>
        </div>
    """, unsafe_allow_html=True)

    with st.expander("💸 Registrar Gasto del Día (Bolsas, movilidad, etc.)"):
        with st.form("form_gastos"):
            desc_gasto = st.text_input("Motivo del gasto:")
            monto_gasto = st.number_input("Monto (S/):", min_value=0.0, step=0.50)
            btn_gasto = st.form_submit_button("Registrar Gasto")
            if btn_gasto and desc_gasto:
                ahora = obtener_tiempo_peru()
                st.session_state.gastos.append({
                    "Fecha_Hora": ahora.strftime("%Y-%m-%d %H:%M"),
                    "Fecha": ahora.strftime("%Y-%m-%d"),
                    "Descripción": desc_gasto,
                    "Monto": monto_gasto
                })
                st.success(f"Gasto de S/ {monto_gasto:.2f} registrado.")

    fecha_hoy = obtener_tiempo_peru().strftime("%Y-%m-%d")
    
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
    with col1:
        st.metric(label="💰 Total Vendido", value=f"S/ {total_ventas_hoy:.2f}")
    with col2:
        st.metric(label="💵 Efec / 📱 Yape", value=f"S/ {efectivo_hoy:.1f} / S/ {yape_hoy:.1f}")
    with col3:
        st.metric(label="📉 Gastos", value=f"S/ {total_gastos_hoy:.2f}")

    st.success(f"🌟 **Ganancia Neta del Día:** S/ {ganancia_neta_hoy:.2f}")

    st.markdown("---")

    if st.button("📄 Generar y Mostrar Reporte Diario Oficial", use_container_width=True):
        st.markdown(f"""
        <div class="report-box">
            <h3 style="color: #0f766e; margin-top: 0;">🏪 MINIMARKET VEGA - REPORTE OFICIAL DE CAJA</h3>
            <p><b>Fecha de Emisión:</b> {obtener_tiempo_peru().strftime('%Y-%m-%d %H:%M:%S')}</p>
            <hr style="border: 0; border-top: 1px solid #cbd5e1;">
            <p><b>💰 Total de Ventas en el Día:</b> S/ {total_ventas_hoy:.2f}</p>
            <p><b>💵 Ingresos en Efectivo:</b> S/ {efectivo_hoy:.2f}</p>
            <p><b>📱 Ingresos por Yape / Plin:</b> S/ {yape_hoy:.2f}</p>
            <p><b>📉 Total de Gastos Operativos:</b> S/ {total_gastos_hoy:.2f}</p>
            <p><b>✨ Ganancia Neta Final:</b> S/ {ganancia_neta_hoy:.2f}</p>
            <hr style="border: 0; border-top: 1px solid #cbd5e1;">
            <p style="font-size: 12px; color: #64748b; text-align: center; margin-bottom: 0;">Reporte generado automáticamente por el sistema del Minimarket Vega.</p>
        </div>
        """, unsafe_allow_html=True)

    ahora_peru = obtener_tiempo_peru()
    texto_wsp = f"*🏪 MINIMARKET VEGA - REPORTE DIARIO*\n" \
                f"📅 *Fecha:* {fecha_hoy} | ⏰ *Hora:* {ahora_peru.strftime('%H:%M')}\n\n" \
                f"💰 *Total Vendido:* S/ {total_ventas_hoy:.2f}\n" \
                f"💵 *Efectivo:* S/ {efectivo_hoy:.2f}\n" \
                f"📱 *Yape / Plin:* S/ {yape_hoy:.2f}\n" \
                f"📉 *Total Gastos:* S/ {total_gastos_hoy:.2f}\n" \
                f"🌟 *Ganancia Neta:* S/ {ganancia_neta_hoy:.2f}\n\n" \
                f"--- *DETALLE DE VENTAS* ---\n"
    
    if ventas_hoy:
        for v in ventas_hoy:
            texto_wsp += f"• {v['Producto']} (x{v['Cantidad']}) - S/ {v['Total']:.2f} [{v['Pago']}]\n"
    else:
        texto_wsp += "No hay ventas registradas.\n"

    texto_wsp += f"\n--- *DETALLE DE GASTOS* ---\n"
    if gastos_hoy:
        for g in gastos_hoy:
            texto_wsp += f"• {g['Descripción']} - S/ {g['Monto']:.2f}\n"
    else:
        texto_wsp += "No hay gastos registrados.\n"

    texto_wsp_encoded = urllib.parse.quote(texto_wsp)
    url_whatsapp = f"https://api.whatsapp.com/send?phone={NUMERO_WHATSAPP}&text={texto_wsp_encoded}"

    st.markdown(f"""
        <a href="{url_whatsapp}" target="_blank" style="text-decoration: none;">
            <div style="background-color: #25d366; color: white; padding: 12px 20px; border-radius: 8px; text-align: center; font-weight: bold; font-size: 16px; margin-top: 15px; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
                💬 Enviar Reporte Completo a mi WhatsApp
            </div>
        </a>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.subheader("🧾 Detalle de Ventas de Hoy")
    if len(ventas_hoy) > 0:
        st.dataframe(pd.DataFrame(ventas_hoy), use_container_width=True)
    else:
        st.info("Aún no hay ventas registradas hoy.")

    st.subheader("🧾 Detalle de Gastos de Hoy")
    if len(gastos_hoy) > 0:
        st.dataframe(pd.DataFrame(gastos_hoy), use_container_width=True)
    else:
        st.info("Aún no hay gastos registrados hoy.")

# ==========================================
# OPCIÓN 5: REPORTE SEMANAL Y MENSUAL
# ==========================================
elif menu == "📅 Reporte Semanal y Mensual":
    st.markdown("""
        <div class="main-header">
            <h1>📅 Balance Semanal y Mensual</h1>
            <p>Evolución de ventas y ganancias acumuladas.</p>
        </div>
    """, unsafe_allow_html=True)

    if len(st.session_state.ventas) == 0 and len(st.session_state.gastos) == 0:
        st.warning("Todavía no hay suficientes registros para calcular reportes.")
    else:
        df_v_total = pd.DataFrame(st.session_state.ventas)
        df_g_total = pd.DataFrame(st.session_state.gastos)

        tipo_reporte = st.radio("Seleccione periodo:", ["📅 Mes Actual", "📆 Últimos 7 Días"], horizontal=True)
        hoy = obtener_tiempo_peru()

        if tipo_reporte == "📅 Mes Actual":
            mes_actual_str = hoy.strftime("%Y-%m")
            v_filtrado = df_v_total[df_v_total["Fecha"].str.startswith(mes_actual_str)] if not df_v_total.empty else pd.DataFrame()
            g_filtrado = df_g_total[df_g_total["Fecha"].str.startswith(mes_actual_str)] if not df_g_total.empty else pd.DataFrame()
        else:
            if not df_v_total.empty:
                df_v_total["Fecha_dt"] = pd.to_datetime(df_v_total["Fecha"])
                hace_7_dias = pd.Timestamp(hoy.date()) - pd.Timedelta(days=7)
                v_filtrado = df_v_total[df_v_total["Fecha_dt"] >= hace_7_dias]
            else:
                v_filtrado = pd.DataFrame()

            if not df_g_total.empty:
                df_g_total["Fecha_dt"] = pd.to_datetime(df_g_total["Fecha"])
                hace_7_dias = pd.Timestamp(hoy.date()) - pd.Timedelta(days=7)
                g_filtrado = df_g_total[df_g_total["Fecha_dt"] >= hace_7_dias]
            else:
                g_filtrado = pd.DataFrame()

        t_ventas = v_filtrado["Total"].sum() if not v_filtrado.empty else 0.0
        t_ganancia_bruta = v_filtrado["Ganancia"].sum() if not v_filtrado.empty else 0.0
        t_gastos = g_filtrado["Monto"].sum() if not g_filtrado.empty else 0.0
        t_ganancia_neta = t_ganancia_bruta - t_gastos

        c1, c2, c3 = st.columns(3)
        with c1:
            st.metric(label="💰 Vendido", value=f"S/ {t_ventas:.2f}")
        with c2:
            st.metric(label="📉 Gastos", value=f"S/ {t_gastos:.2f}")
        with c3:
            st.metric(label="🌟 Neta Acumulada", value=f"S/ {t_ganancia_neta:.2f}")

        st.markdown("---")
        st.subheader("📋 Ventas del Periodo")
        if not v_filtrado.empty:
            cols_mostrar = [c for c in ["Fecha_Hora", "Producto", "Cantidad", "Total", "Ganancia", "Pago"] if c in v_filtrado.
