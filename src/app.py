import streamlit as st
import pandas as pd
from sqlalchemy.orm import Session
from models import FinancialData, engine, init_db
from finance_data import get_financial_data
from db_operations import insert_financial_data

# Inicializar la base de datos
init_db()

st.title('Financial Data Analyzer')

# Input para el símbolo del ticker
ticker_symbol = st.text_input('Enter a ticker symbol (e.g., MCD for McDonald\'s):', 'MCD')

if st.button('Fetch and Analyze Data'):
    try:
        # Obtener datos financieros
        financial_data = get_financial_data(ticker_symbol)
        
        if financial_data.empty:
            st.error(f"No se pudieron obtener datos financieros para {ticker_symbol}. Por favor, verifica el símbolo del ticker.")
        else:
            # Insertar datos en la base de datos
            insert_financial_data(financial_data, ticker_symbol)
            
            # Mostrar los datos
            st.write(f"Financial data for {ticker_symbol}:")
            st.dataframe(financial_data)
            
            # Agregar más análisis y visualizaciones aquí
            if 'Sales' in financial_data.columns:
                st.line_chart(financial_data['Sales'])
            if 'Net Margin %' in financial_data.columns:
                st.line_chart(financial_data['Net Margin %'])
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")

# Función para mostrar datos históricos
def show_historical_data():
    session = Session(bind=engine)
    data = session.query(FinancialData).all()
    df = pd.DataFrame([vars(d) for d in data])
    session.close()
    
    st.write("Historical Financial Data:")
    st.dataframe(df)

if st.button('Show Historical Data'):
    show_historical_data()