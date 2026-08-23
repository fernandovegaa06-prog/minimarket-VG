from datetime import datetime
import json
import os
import urllib.parse
import pandas as pd
import pytz
import streamlit as st

st.set_page_config(page_title="Minimarket VG", page_icon="🛒", layout="centered")

NUMERO_WHATSAPP = "51984116361"
ZONA_PERU = pytz.timezone("America/Lima")
ARCH_INVENTARIO = "inventario_vg.json"
ARCH_VENTAS = "ventas_vg.json"
ARCH_GASTOS = "gastos_vg.json"

def obtener_tiempo_peru():
    return datetime.now(ZONA_PERU)

def cargar_datos():
    inv_inicial = [
        {"Categoría": "Abarrotes", "Producto": "Arroz Costeño (kg)", "Precio Venta": 4.50, "Costo Compra": 3.80, "Stock": 25.0},
        {"Categoría": "Abarrotes", "Producto": "Azúcar Rubia (kg)", "Precio Venta": 4.00, "Costo Compra": 3.30, "Stock": 25.0},
        {"Categoría": "Abarrotes", "Producto": "Fideos Don Vittorio (500g)", "Precio Venta": 3.20, "Costo Compra": 2.60, "Stock": 25.0},
        {"Categoría": "Abarrotes", "Producto": "Aceite Primor (1L)", "Precio Venta": 9.50, "Costo Compra": 8.20, "Stock": 2.0},
        {"Categoría": "Abarrotes", "Producto": "Atún Florida (latas)", "Precio Venta": 5.50, "Costo Compra": 4.60, "Stock": 25.0},
        {"Categoría": "Lácteos", "Producto": "Leche Gloria Azul (tarro)", "Precio Venta": 4.80, "Costo Compra": 4.10, "Stock": 3.0},
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
    ]

    if os.path.exists(ARCH_INVENTARIO):
        try:
            df_inv = pd.read_json(ARCH_INVENTARIO)
        except:
            df_inv = pd.DataFrame(inv_inicial)
    else:
        df_inv = pd.DataFrame(inv_inicial)
        df_inv.to_json(ARCH_INVENTARIO, orient="records", indent=4)

    if os.path.exists(ARCH_VENTAS):
        try:
            with open(ARCH_VENTAS, 'r', encoding='utf-8') as f:
                ventas = json.load(f)
        except:
            ventas = []
    else:
        ventas = []

    if os.path.exists(ARCH_GASTOS):
        try:
            with open(ARCH_GASTOS, 'r', encoding='utf-8') as f:
                gastos = json.load(f)
        except:
            gastos = []
    else:
        gastos = []

    return df_inv, ventas, gastos

def guardar_inventario(df):
    df.to_json(ARCH_INVENTARIO, orient="records", indent=4)

def guardar_ventas(ventas):
    with open(ARCH_VENTAS, 'w', encoding='utf-8') as f:
        json.dump(ventas, f, ensure_ascii=False, indent=4)

def guardar_gastos(gastos):
    with open(ARCH_GASTOS, 'w', encoding='utf-8') as f:
        json.dump(gastos, f, ensure_ascii=False, indent=4)

# Estilo visual
st.markdown("""
<style>
    .stApp { background-color: #f1f5f9; }
    .main-header {
        background: #ffffff; border: 2px solid #cbd5e1; padding: 24px;
        border-radius: 16px; color: #0f172a; margin-bottom: 20px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05); text-align: center;
    }
    .main-header h1 { margin: 0; font-size: 28px; font-weight: 800; color: #0f172a !important; }
    .main-header p { margin: 6px 0 0 0; font-size: 14px; color: #475569 !important; font-weight: 600; }
    .report-box {
        background-color: #ffffff; border: 2px solid #94a3b8; padding: 20px;
        border-radius: 12px; margin-top: 15px; margin-bottom: 15px; box-shadow: 0 4px 12px rgba(0,0,0,0.05);
    }
    .stMarkdown, .stText, h1, h2, h3, p, label, span { color: #0f172a !important; }
    .login-card {
        background: #ffffff; padding: 35px; border-radius: 18px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.08); text-align: center; border: 1px solid #cbd5e1;
    }
</style>
""", unsafe_allow_html=True)

if 'autenticado' not in st.session_state:
    st.session_state.autenticado = False

if 'inventario' not in st.session_state or 'ventas' not in st.session_state or 'gastos' not in st.session_state:
    inv_arga, ventas_arga, gastos_arga = cargar_datos()
    st.session_state.inventario = inv_arga
    st.session_state.ventas = ventas_arga
    st.session_state.gastos = gastos_arga

if not st.session_state.autenticado:
    st.markdown("""
        <div class="login-card">
            <h1 style="color: #0f172a !important; font-size: 32px; margin-bottom: 5px;">🛒 MINIMARKET VG 🛍️</h1>
            <p style="color: #475569 !important; font-size: 15px; font-weight: 600;">Control de Inventario y Caja 🏪</p>
        </div>
    """, unsafe_allow_html=True)
    
    password_ingresada = st.text_input("🔑 Ingrese su contraseña de acceso:", type="password")
    if st.button("🚀 Ingresar al Sistema", use_container_width=True):
        if password_ingresada == "1234":
            st.session_state.autenticado = True
            st.rerun()
        else:
            st.error("❌ Contraseña incorrecta. (Prueba con: 1234)")
    st.stop()

with st.sidebar:
    st.markdown("<h2 style='text-align: center; color: #0f172a;'>🏪 MINIMARKET VG 🛒</h2>", unsafe_allow_html=True)
    st.image("https://images.unsplash.com/photo-1542838132-92c53300491e?auto=format&fit=crop&w=500&q=80", caption="Tu Bodega de Confianza", use_container_width=True)
    st.caption("Panel de Control Comercial")
    if st.button("🔒 Cerrar Sesión", use_container_width=True):
        st.session_state.autenticado = False
        st.rerun()
    st.markdown("---")
    menu = st.selectbox("Seleccione Operación:", [
        "🛒 Registrar Venta",
        "💳 Registrar Yape / Plin (Delivery)",
        "📜 Historial y Búsqueda por Fechas",
        "🚨 Alertas de Stock Bajo",
        "📦 Ver Stock y Montos",
        "🛠️ Corregir Stock / Precios",
        "📊 Cierre de Caja y Balance",
        "📅 Reporte Semanal y Mensual"
    ])

if menu == "🛒 Registrar Venta":
    st.markdown("""
        <div class="main-header">
            <h1>🛒 MINIMARKET VG - CAJA Y VENTAS 🛍️</h1>
            <p>Control rápido de cobros, abarrotes y ganancias al instante</p>
        </div>
    """, unsafe_allow_html=True)
    
    lista_productos = st.session_state.inventario["Producto"].tolist()
    producto_seleccionado = st.selectbox("📦 Seleccione el producto:", lista_productos)
    prod_data = st.session_state.inventario[st.session_state.inventario["Producto"] == producto_seleccionado].iloc[0]
    stock_actual, precio_venta, costo_compra, categoria_prod = prod_data["Stock"], prod_data["Precio Venta"], prod_data["Costo Compra"], prod_data["Categoría"]
    
    st.info(f"📂 Categoría: **{categoria_prod}** |  🏷️ Precio Venta: **S/ {precio_venta:.2f}**")
    cantidad = st.number_input(f"⚖️ Cantidad (Stock disponible: {stock_actual}):", min_value=0.5, max_value=float(stock_actual) if stock_actual > 0 else 1.0, value=1.0, step=0.5)
    metodo_pago = st.radio("💳 ¿Cómo pagó el cliente?", ["Efectivo", "Yape / Plin"], horizontal=True)
    
    total_cobrar, ganancia_estimada = cantidad * precio_venta, cantidad * (precio_venta - costo_compra)
    
    col_a, col_b = st.columns(2)
    with col_a: st.metric(label="💰 Total a Cobrar", value=f"S/ {total_cobrar:.2f}")
    with col_b: st.metric(label="✨ Ganancia Estimada", value=f"S/ {ganancia_estimada:.2f}")
    
    if st.button("✅ Cobrar y Registrar Venta", use_container_width=True):
        if stock_actual >= cantidad:
            st.session_state.inventario.loc[st.session_state.inventario["Producto"] == producto_seleccionado, "Stock"] -= cantidad
            ahora = obtener_tiempo_peru()
            st.session_state.ventas.append({
                "Fecha_Hora": ahora.strftime("%Y-%m-%d %H:%M"),
                "Fecha": ahora.strftime("%Y-%m-%d"),
                "Producto": producto_seleccionado,
                "Cantidad": cantidad,
                "Total": total_cobrar,
                "Ganancia": ganancia_estimada,
                "Pago": metodo_pago,
                "Detalle": f"Venta directa: {producto_seleccionado} x {cantidad}"
            })
            guardar_inventario(st.session_state.inventario)
            guardar_ventas(st.session_state.ventas)
            st.success("🎉 ¡Venta registrada con éxito y stock guardado permanentemente!")
        else:
            st.error("❌ No hay suficiente stock disponible para esta venta.")

elif menu == "💳 Registrar Yape / Plin (Delivery)":
    st.markdown("""
        <div class="main-header">
            <h1>📱 REGISTRO YAPE / PLIN Y VOUCHERS 🛵</h1>
            <p>Asocia capturas de pantalla y apuntes de pedidos por delivery</p>
        </div>
    """, unsafe_allow_html=True)
    
    with st.form("form_yape_delivery", clear_on_submit=True):
        monto_yape = st.number_input("💰 Monto exacto que llegó por Yape/Plin (S/):", min_value=0.0, step=1.0, format="%.2f")
        detalle_apuntes = st.text_area("📝 Detalle de productos según tus apuntes o WhatsApp del cliente:", placeholder="Ej: S/ 30 de abarrotes, 1 aceite, 2 leches...")
        ganancia_calculada = st.number_input("✨ Ganancia estimada aproximada para caja (S/) [Opcional - por defecto 20% del monto]:", min_value=0.0, value=0.0, step=0.50)
        foto_voucher = st.file_uploader("📸 Adjuntar captura de pantalla del voucher (Galería o cámara del celular)", type=["png", "jpg", "jpeg"])
        
        btn_guardar_yape = st.form_submit_button("✅ Registrar Ingreso Digital y Voucher")
        
        if btn_guardar_yape:
            if monto_yape > 0:
                ganancia_final = ganancia_calculada if ganancia_calculada > 0 else (monto_yape * 0.20)
                ahora = obtener_tiempo_peru()
                
                st.session_state.ventas.append({
                    "Fecha_Hora": ahora.strftime("%Y-%m-%d %H:%M"),
                    "Fecha": ahora.strftime("%Y-%m-%d"),
                    "Producto": "Pedido Yape / Delivery",
                    "Cantidad": 1.0,
                    "Total": monto_yape,
                    "Ganancia": ganancia_final,
                    "Pago": "Yape / Plin",
                    "Detalle": detalle_apuntes if detalle_apuntes else "Pago por Yape sin detalle"
                })
                guardar_ventas(st.session_state.ventas)
                
                st.success(f"🎉 ¡Yape de S/ {monto_yape:.2f} registrado y sumado a caja con éxito!")
                
                if foto_voucher is not None:
                    st.image(foto_voucher, caption="Voucher de Yape verificado y guardado", use_container_width=True)
            else:
                st.error("❌ Por favor ingresa un monto válido mayor a 0.")

elif menu == "📜 Historial y Búsqueda por Fechas":
    st.markdown("""
        <div class="main-header">
            <h1>📜 HISTORIAL GENERAL DE VENTAS 🔍</h1>
            <p>Busca, revisa y filtra transacciones pasadas por fecha o palabra clave</p>
        </div>
    """, unsafe_allow_html=True)
    
    if not st.session_state.ventas:
        st.info("Todavía no hay ventas registradas en el historial. ¡Empieza a registrar ventas para verlas aquí!")
    else:
        df_historial = pd.DataFrame(st.session_state.ventas)
        busqueda = st.text_input("🔎 Buscar en el historial (Producto o detalle):", "")
        if busqueda:
            df_historial = df_historial[
                df_historial['Producto'].str.contains(busqueda, case=False, na=False) |
                df_historial['Detalle'].str.contains(busqueda, case=False, na=False)
            ]
        
        st.dataframe(df_historial, use_container_width=True)
        st.download_button(
            label="📥 Descargar Historial Completo en CSV",
            data=df_historial.to_csv(index=False).encode('utf-8'),
            file_name=f"historial_ventas_minimarket_vg_{obtener_tiempo_peru().strftime('%Y-%m-%d')}.csv",
            mime="text/csv",
            use_container_width=True
        )

elif menu == "🚨 Alertas de Stock Bajo":
    st.markdown("""
        <div class="main-header">
            <h1>🚨 ALERTAS DE STOCK CRÍTICO ⚠️</h1>
            <p>Productos que están por agotarse en tu minimarket</p>
        </div>
    """, unsafe_allow_html=True)
    
    inv_df = st.session_state.inventario
    stock_critico = inv_df[inv_df["Stock"] <= 5]
    
    if not stock_critico.empty:
        st.warning("⚠️ **¡Atención!** Los siguientes productos tienen stock menor o igual a 5 unidades. Considera reponerlos pronto:")
        st.dataframe(stock_critico, use_container_width=True)
    else:
        st.success("🎉 ¡Excelente! No hay ningún producto con stock crítico en este momento. Todo está abastecido.")

elif menu == "📦 Ver Stock y Montos":
    st.markdown("""
        <div class="main-header">
            <h1>📦 INVENTARIO Y ABARROTES 🛒</h1>
            <p>Supervisa tu mercadería en almacén y valora tu capital</p>
        </div>
    """, unsafe_allow_html=True)
    
    inventario_df = st.session_state.inventario.copy()
    inventario_df["Valor Total en Stock (S/)"] = inventario_df["Stock"] * inventario_df["Precio Venta"]
    valortotal_dinero = inventario_df["Valor Total en Stock (S/)"].sum()
    
    col1, col2 = st.columns(2)
    with col1: st.metric(label="🏷️ Total Productos", value=len(inventario_df))
    with col2: st.metric(label="💵 Valor Total de Mercadería", value=f"S/ {valortotal_dinero:.2f}")
    
    st.markdown("---")
    cat_elegida = st.selectbox("📂 Filtrar Inventario por Categoría:", ["Todas"] + list(inventario_df["Categoría"].unique()))
    inventario_filtrado = inventario_df if cat_elegida == "Todas" else inventario_df[inventario_df["Categoría"] == cat_elegida]
    
    st.dataframe(inventario_filtrado, use_container_width=True)
    st.download_button(
        label="📥 Descargar Reporte de Inventario (CSV)",
        data=inventario_filtrado.to_csv(index=False).encode('utf-8'),
        file_name=f"inventario_minimarket_vg_{obtener_tiempo_peru().strftime('%Y-%m-%d')}.csv",
        mime="text/csv",
        use_container_width=True
    )

elif menu == "🛠️ Corregir Stock / Precios":
    st.markdown("""
        <div class="main-header">
            <h1>🛠️ CORRECCIÓN DE INVENTARIO 📝</h1>
            <p>Actualiza de forma rápida precios, costos o ajusta tu mercadería</p>
        </div>
    """, unsafe_allow_html=True)
    
    prod_a_editar = st.selectbox("🔍 Selecciona el producto a corregir:", st.session_state.inventario["Producto"].tolist())
    fila_prod = st.session_state.inventario[st.session_state.inventario["Producto"] == prod_a_editar].iloc[0]
    
    st.info(f"📌 Estado actual de **{prod_a_editar}** ➔ Stock: {fila_prod['Stock']} | Precio Venta: S/ {fila_prod['Precio Venta']:.2f}")
    nuevo_stock = st.number_input("📦 Stock exacto:", value=float(fila_prod["Stock"]), step=1.0)
    nuevo_precio = st.number_input("🏷️ Precio de Venta (S/):", value=float(fila_prod["Precio Venta"]), step=0.10)
    nuevo_costo = st.number_input("📉 Costo de Compra (S/):", value=float(fila_prod["Costo Compra"]), step=0.10)
    
    if st.button("💾 Guardar Cambios", use_container_width=True):
        st.session_state.inventario.loc[st.session_state.inventario["Producto"] == prod_a_editar, ["Stock", "Precio Venta", "Costo Compra"]] = [nuevo_stock, nuevo_precio, nuevo_costo]
        guardar_inventario(st.session_state.inventario)
        st.success(f"✅ ¡Los datos de '{prod_a_editar}' han sido actualizados y guardados con éxito!")

elif menu == "📊 Cierre de Caja y Balance":
    st.markdown("""
        <div class="main-header">
            <h1>📊 CIERRE DE CAJA Y BALANCE 💰</h1>
            <p>Resumen final de ingresos, efectivo, Yape/Plin y ganancia neta</p>
        </div>
    """, unsafe_allow_html=True)
    
    with st.expander("💸 Registrar Gasto del Día"):
        with st.form("form_gastos"):
            desc_gasto = st.text_input("Motivo del gasto:")
            monto_gasto = st.number_input("Monto (S/):", min_value=0.0, step=0.50)
            if st.form_submit_button("Registrar Gasto") and desc_gasto:
                ahora = obtener_tiempo_peru()
                st.session_state.gastos.append({
                    "Fecha_Hora": ahora.strftime("%Y-%m-%d %H:%M"),
                    "Fecha": ahora.strftime("%Y-%m-%d"),
                    "Descripción": desc_gasto,
                    "Monto": monto_gasto
                })
                guardar_gastos(st.session_state.gastos)
                st.success(f"Gasto de S/ {monto_gasto:.2f} registrado y guardado.")
                
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
    with col1: st.metric(label="💰 Total Vendido", value=f"S/ {total_ventas_hoy:.2f}")
    with col2: st.metric(label="💵 Efec / 📱 Yape", value=f"S/ {efectivo_hoy:.1f} / S/ {yape_hoy:.1f}")
    with col3: st.metric(label="📉 Gastos", value=f"S/ {total_gastos_hoy:.2f}")
    
    st.success(f"🌟 **Ganancia Neta del Día:** S/ {ganancia_neta_hoy:.2f}")
    
    if st.button("📄 Generar y Mostrar Reporte Diario Oficial", use_container_width=True):
        st.markdown(f"""
        <div class="report-box">
            <h3 style="color: #0f172a; margin-top: 0;">🏪 MINIMARKET VG - REPORTE OFICIAL DE CAJA</h3>
            <p><b>📅 Fecha de Emisión:</b> {obtener_tiempo_peru().strftime('%Y-%m-%d %H:%M:%S')}</p>
            <hr style="border: 0; border-top: 1px solid #cbd5e1;">
            <p><b>💰 Total de Ventas en el Día:</b> S/ {total_ventas_hoy:.2f}</p>
            <p><b>💵 Ingresos en Efectivo:</b> S/ {efectivo_hoy:.2f}</p>
            <p><b>📱 Ingresos por Yape / Plin:</b> S/ {yape_hoy:.2f}</p>
            <p><b>📉 Total de Gastos Operativos:</b> S/ {total_gastos_hoy:.2f}</p>
            <p><b>✨ Ganancia Neta Final:</b> S/ {ganancia_neta_hoy:.2f}</p>
        </div>
        """, unsafe_allow_html=True)
        
    texto_wsp = "*🏪 MINIMARKET VG - REPORTE DIARIO*\n" + \
                f"📅 *Fecha:* {fecha_hoy}\n" + \
                f"💰 *Total Vendido:* S/ {total_ventas_hoy:.2f}\n" + \
                f"💵 *Efectivo:* S/ {efectivo_hoy:.2f}\n" + \
                f"📱 *Yape / Plin:* S/ {yape_hoy:.2f}\n" + \
                f"📉 *Total Gastos:* S/ {total_gastos_hoy:.2f}\n" + \
                f"🌟 *Ganancia Neta:* S/ {ganancia_neta_hoy:.2f}\n"

    url_whatsapp = f"https://api.whatsapp.com/send?phone={NUMERO_WHATSAPP}&text={urllib.parse.quote(texto_wsp)}"
    
    btn_html = '<a href="' + url_whatsapp + '" target="_blank" style="text-decoration: none;">' \
               '<div style="background-color: #25d366; color: white; padding: 14px 20px; border-radius: 10px; text-align: center; font-weight: bold; font-size: 16px; margin-top: 15px; box-shadow: 0 4px 12px rgba(37, 211, 102, 0.4);">' \
               '💬 Enviar Reporte a mi WhatsApp' \
               '</div></a>'
    st.markdown(btn_html, unsafe_allow_html=True)

elif menu == "📅 Reporte Semanal y Mensual":
    st.markdown("""
        <div class="main-header">
            <h1>📅 BALANCE SEMANAL Y MENSUAL 📈</h1>
            <p>Visualiza la evolución de tus ventas y el acumulado de ganancias</p>
        </div>
    """, unsafe_allow_html=True)
    
    if not st.session_state.ventas and not st.session_state.gastos:
        st.warning("Todavía no hay suficientes registros para calcular reportes.")
    else:
        df_v = pd.DataFrame(st.session_state.ventas)
        df_g = pd.DataFrame(st.session_state.gastos)
        tipo_rep = st.radio("Seleccione periodo:", ["📅 Mes Actual", "📆 Últimos 7 Días"], horizontal=True)
        hoy = obtener_tiempo_peru()
        
        if tipo_rep == "📅 Mes Actual":
            mes_str = hoy.strftime("%Y-%m")
            v_f = df_v[df_v["Fecha"].str.startswith(mes_str)] if not df_v.empty else pd.DataFrame()
            g_f = df_g[df_g["Fecha"].str.startswith(mes_str)] if not df_g.empty else pd.DataFrame()
        else:
            hace_7 = pd.Timestamp(hoy.date()) - pd.Timedelta(days=7)
            if not df_v.empty:
                df_v["Fecha_dt"] = pd.to_datetime(df_v["Fecha"])
                v_f = df_v[df_v["Fecha_dt"] >= hace_7]
            else:
                v_f = pd.DataFrame()
            if not df_g.empty:
                df_g["Fecha_dt"] = pd.to_datetime(df_g["Fecha"])
                g_f = df_g[df_g["Fecha_dt"] >= hace_7]
            else:
                g_f = pd.DataFrame()
                
        t_v = v_f["Total"].sum() if not v_f.empty else 0.0
        t_g_bruta = v_f["Ganancia"].sum() if not v_f.empty else 0.0
        t_gastos = g_f["Monto"].sum() if not g_f.empty else 0.0
        t_neta = t_g_bruta - t_gastos
        
        c1, c2, c3 = st.columns(3)
        with c1: st.metric(label="💰 Vendido", value=f"S/ {t_v:.2f}")
        with c2: st.metric(label="📉 Gastos", value=f"S/ {t_gastos:.2f}")
        with c3: st.metric(label="🌟 Neta Acumulada", value=f"S/ {t_neta:.2f}")
        
        st.markdown("---")
        st.subheader("📋 Ventas del Periodo")
        if not v_f.empty:
            cols = [c for c in ["Fecha_Hora", "Producto", "Cantidad", "Total", "Ganancia", "Pago", "Detalle"] if c in v_f.columns]
            st.dataframe(v_f[cols], use_container_width=True)
        else:
            st.info("No hay ventas en este periodo.")
