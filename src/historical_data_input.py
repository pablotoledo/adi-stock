import streamlit as st
import pandas as pd

def historical_data_input():
    st.subheader("Ingrese los datos históricos")
    
    years = st.number_input("Número de años de datos históricos", min_value=1, max_value=10, value=5)
    
    data = {}
    for year in range(years):
        st.subheader(f"Año {2023 - year}")
        data[f"{2023 - year}"] = {
            "Ventas": st.number_input(f"Ventas {2023 - year}", min_value=0.0, format="%.2f", key=f"sales_{year}"),
            "Beneficio Operativo": st.number_input(f"Beneficio Operativo {2023 - year}", format="%.2f", key=f"operating_profit_{year}"),
            "Depreciación y Amortización": st.number_input(f"Depreciación y Amortización {2023 - year}", min_value=0.0, format="%.2f", key=f"depreciation_{year}"),
            "Ingresos/Gastos Financieros": st.number_input(f"Ingresos/Gastos Financieros {2023 - year}", format="%.2f", key=f"financial_{year}"),
            "Impuestos": st.number_input(f"Impuestos {2023 - year}", min_value=0.0, format="%.2f", key=f"taxes_{year}"),
            "Número de Acciones": st.number_input(f"Número de Acciones {2023 - year}", min_value=0.0, format="%.2f", key=f"shares_{year}")
        }
    
    df = pd.DataFrame(data).T
    st.write(df)
    
    return df