import streamlit as st
import pandas as pd
import urllib.parse

st.set_page_config(page_title="Minimarket Vega", page_icon="🛒", layout="centered")

NUMERO_WHATSAPP = "51984116361"

st.title("🛒 Minimarket Vega - Sistema de Gestión")

# Inicializar datos
if 'inventario' not in st.session_state:
    st.session_state.inventario = pd.DataFrame([
        {"Categoría": "Abarrotes", "Producto": "Arroz Costeño (kg)", "Precio Venta": 4.50, "Costo Compra": 3.80, "Stock": 25.0},
        {"Categoría": "Abarrotes", "Producto": "Azúcar Rubia (kg)", "Precio Venta": 4.00, "Costo Compra": 3.30, "Stock": 25.0},
        {"Categoría": "Lácteos", "Producto": "Leche Gloria Azul (tarro)", "Precio Venta": 4.80, "Costo Compra": 4.10, "Stock": 25.0},
        {"Categoría": "Bebidas", "Producto": "Inca Kola (1.5L)", "Precio Venta": 7.50, "Costo Compra": 6.20, "Stock": 25.0}
    ])

if 'ventas' not in st.session_state:
    st.session_state.ventas = []

if 'gastos' not in st.session_state:
    st.session_state.gastos = []

menu = st.sidebar.selectbox("Seleccione:", ["📦 Ver Inventario", "🛒 Registrar Venta", "📊 Cierre de Caja y Balance"])

if menu == "📦 Ver Inventario":
    st.subheader("📦 Productos en Stock")
    st.dataframe(st.session_state.inventario, use_container_width=True)

elif menu == "🛒 Registrar Venta":
    st.subheader("🛒 Registrar una Venta")
    lista_productos = st.session_state.inventario["Producto"].tolist()
    producto_seleccionado = st.selectbox("Seleccione el producto:", lista_productos)
    
    prod_data = st.session_state.inventario[st.session_state.inventario["Producto"] == producto_seleccionado].iloc[0]
    stock_actual, precio_venta, costo_compra = prod_data["Stock"], prod_data["Precio Venta"], prod_data["Costo Compra"]
    
    st.info(f"Stock disponible: {stock_actual} | Precio: S/ {precio_venta:.2f}")
    cantidad = st.number_input("Cantidad a vender:", min_value=0.5, max_value=float(stock_actual) if stock_actual > 0 else 1.0, value=1.0, step=0.5)
    
    total_cobrar = cantidad * precio_venta
    ganancia_estimada = cantidad * (precio_venta - costo_compra)
    st.metric(label="Total a Cobrar", value=f"S/ {total_cobrar:.2f}")
    
    if st.button("✅ Cobrar y Descontar Stock", use_container_width=True):
        if stock_actual >= cantidad:
            st.session_state.inventario.loc[st.session_state.inventario["Producto"] == producto_seleccionado, "Stock"] -= cantidad
            st.session_state.ventas.append({
                "Producto": producto_seleccionado, "Cantidad": cantidad, 
                "Total": total_cobrar, "Ganancia": ganancia_estimada
            })
            st.success("🎉 ¡Venta registrada con éxito!")
        else:
            st.error("❌ No hay suficiente stock disponible.")

    if len(st.session_state.ventas) > 0:
        st.markdown("---")
        st.subheader("📋 Ventas Registradas")
        st.dataframe(pd.DataFrame(st.session_state.ventas), use_container_width=True)

elif menu == "📊 Cierre de Caja y Balance":
    st.subheader("📊 Balance y Cierre de Caja")
    
    with st.expander("💸 Registrar Gasto del Día"):
        with st.form("form_gastos"):
            desc_gasto = st.text_input("Motivo del gasto:")
            monto_gasto = st.number_input("Monto (S/):", min_value=0.0, step=0.50)
            if st.form_submit_button("Registrar Gasto") and desc_gasto:
                st.session_state.gastos.append({"Descripción": desc_gasto, "Monto": monto_gasto})
                st.success(f"Gasto de S/ {monto_gasto:.2f} registrado.")

    total_ventas = sum(v["Total"] for v in st.session_state.ventas) if st.session_state.ventas else 0.0
    total_ganancia = sum(v["Ganancia"] for v in st.session_state.ventas) if st.session_state.ventas else 0.0
    total_gastos = sum(g["Monto"] for g in st.session_state.gastos) if st.session_state.gastos else 0.0
    ganancia_neta = total_ganancia - total_gastos

    col1, col2 = st.columns(2)
    with col1: st.metric(label="💰 Total Vendido", value=f"S/ {total_ventas:.2f}")
    with col2: st.metric(label="📉 Total Gastos", value=f"S/ {total_gastos:.2f}")
    
    st.success(f"🌟 **Ganancia Neta:** S/ {ganancia_neta:.2f}")

    texto_wsp = f"*🏪 MINIMARKET VEGA - REPORTE*\n💰 *Total Vendido:* S/ {total_ventas:.2f}\n📉 *Gastos:* S/ {total_gastos:.2f}\n🌟 *Ganancia Neta:* S/ {ganancia_neta:.2f}"
    url_whatsapp = f"https://api.whatsapp.com/send?phone={NUMERO_WHATSAPP}&text={urllib.parse.quote(texto_wsp)}"
    
    st.markdown(f"""<a href="{url_whatsapp}" target="_blank" style="text-decoration: none;"><div style="background-color: #25d366; color: white; padding: 12px 20px; border-radius: 8px; text-align: center; font-weight: bold; margin-top: 15px;">💬 Enviar Reporte a WhatsApp</div></a>""", unsafe_allow_html=True)
