import streamlit as st
import pandas as pd

st.set_page_config(page_title="Minimarket Vega", page_icon="🛒", layout="centered")

st.title("🛒 Minimarket Vega - Sistema de Caja")

# Inicializar inventario y ventas
if 'inventario' not in st.session_state:
    st.session_state.inventario = pd.DataFrame([
        {"Categoría": "Abarrotes", "Producto": "Arroz Costeño (kg)", "Precio Venta": 4.50, "Costo Compra": 3.80, "Stock": 25.0},
        {"Categoría": "Abarrotes", "Producto": "Azúcar Rubia (kg)", "Precio Venta": 4.00, "Costo Compra": 3.30, "Stock": 25.0},
        {"Categoría": "Lácteos", "Producto": "Leche Gloria Azul (tarro)", "Precio Venta": 4.80, "Costo Compra": 4.10, "Stock": 25.0},
        {"Categoría": "Bebidas", "Producto": "Inca Kola (1.5L)", "Precio Venta": 7.50, "Costo Compra": 6.20, "Stock": 25.0}
    ])

if 'ventas' not in st.session_state:
    st.session_state.ventas = []

# Menú lateral simple
menu = st.sidebar.selectbox("Seleccione:", ["📦 Ver Inventario", "🛒 Registrar Venta"])

if menu == "📦 Ver Inventario":
    st.subheader("📦 Productos en Stock")
    st.dataframe(st.session_state.inventario, use_container_width=True)

elif menu == "🛒 Registrar Venta":
    st.subheader("🛒 Registrar una Venta")
    
    lista_productos = st.session_state.inventario["Producto"].tolist()
    producto_seleccionado = st.selectbox("Seleccione el producto:", lista_productos)
    
    prod_data = st.session_state.inventario[st.session_state.inventario["Producto"] == producto_seleccionado].iloc[0]
    stock_actual = prod_data["Stock"]
    precio_venta = prod_data["Precio Venta"]
    
    st.info(f"Stock disponible: {stock_actual} | Precio: S/ {precio_venta:.2f}")
    
    cantidad = st.number_input("Cantidad a vender:", min_value=0.5, max_value=float(stock_actual) if stock_actual > 0 else 1.0, value=1.0, step=0.5)
    
    total_cobrar = cantidad * precio_venta
    st.metric(label="Total a Cobrar", value=f"S/ {total_cobrar:.2f}")
    
    if st.button("✅ Cobrar y Descontar Stock", use_container_width=True):
        if stock_actual >= cantidad:
            # Descontar stock
            st.session_state.inventario.loc[st.session_state.inventario["Producto"] == producto_seleccionado, "Stock"] -= cantidad
            
            # Registrar venta
            st.session_state.ventas.append({
                "Producto": producto_seleccionado,
                "Cantidad": cantidad,
                "Total": total_cobrar
            })
            st.success("🎉 ¡Venta registrada con éxito!")
        else:
            st.error("❌ No hay suficiente stock disponible.")

    if len(st.session_state.ventas) > 0:
        st.markdown("---")
        st.subheader("📋 Ventas realizadas hoy")
        st.dataframe(pd.DataFrame(st.session_state.ventas), use_container_width=True)
