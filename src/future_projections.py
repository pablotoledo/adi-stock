import streamlit as st

def future_projections():
    st.subheader("Proyecciones Futuras")
    
    years = st.number_input("Años de proyección", min_value=1, max_value=10, value=5)
    
    growth_rate = st.number_input("Tasa de crecimiento anual (%)", min_value=0.0, max_value=100.0, value=7.0)
    operating_margin = st.number_input("Margen operativo (%)", min_value=0.0, max_value=100.0, value=10.5)
    tax_rate = st.number_input("Tasa impositiva (%)", min_value=0.0, max_value=100.0, value=27.5)
    
    return years, growth_rate, operating_margin, tax_rate