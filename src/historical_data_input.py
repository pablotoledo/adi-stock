import streamlit as st
import pandas as pd

def historical_data_input(loaded_data=None):
    st.subheader("Datos Históricos")
    
    # Si hay datos cargados automáticamente, los usamos como base
    if loaded_data is not None:
        historical_data = loaded_data.copy()
    else:
        # Si no hay datos cargados, creamos un DataFrame vacío
        historical_data = pd.DataFrame(columns=[
            'Año', 'Ventas', 'Beneficio Operativo', 'Depreciación y Amortización',
            'Intereses', 'Impuestos', 'Número de Acciones'
        ])
        for year in range(2015, 2022):
            historical_data = historical_data.append({'Año': year}, ignore_index=True)
    
    # Permitir al usuario editar los datos
    edited_data = st.data_editor(historical_data)
    
    if st.button("Guardar Datos Históricos"):
        st.success("Datos históricos guardados exitosamente")
        return edited_data
    
    return None