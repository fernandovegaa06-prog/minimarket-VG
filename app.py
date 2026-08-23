import streamlit as st
import pandas as pd

st.set_page_config(page_title="Minimarket Vega", page_icon="🛒", layout="centered")

st.title("🛒 Minimarket Vega - Control de Inventario")

# Inicializar inventario
if 'inventario' not in st.session_state:
    st.session_state.inventario = pd.DataFrame([
        {"Categoría": "Abarrotes", "Producto": "Arroz Costeño (kg)", "Precio Venta": 4.50, "Costo Compra": 3.80, "Stock": 25.0},
        {"Categoría": "Abarrotes", "Producto": "Azúcar Rubia (kg)", "Precio Venta": 4.00, "Costo Compra": 3.30, "Stock": 25.0},
        {"Categoría": "Lácteos", "Producto": "Leche Gloria Azul (tarro)", "Precio Venta": 4.80, "Costo Compra": 4.10, "Stock": 25.0},
        {"Categoría": "Bebidas", "Producto": "Inca Kola (1.5L)", "Precio Venta": 7.50, "Costo Compra": 6.20, "Stock": 25.0}
    ])

st.success("¡Base de datos de productos cargada con éxito!")

# Mostrar tabla de productos
st.subheader("📦 Productos en Stock")
st.dataframe(st.session_state.inventario, use_container_width=True)
