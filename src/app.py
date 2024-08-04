import streamlit as st
import pandas as pd
from sqlalchemy.orm import Session
from models import FinancialData, engine, init_db, print_schema, drop_tables
from finance_data import get_financial_data
from db_operations import insert_financial_data
from utils.logger import logger

# Inicializar la base de datos
init_db()
logger.info("Database initialized")

st.title('Financial Data Analyzer')

# Input para el símbolo del ticker
ticker_symbol = st.text_input('Enter a ticker symbol (e.g., MCD for McDonald\'s):', 'MCD')

if st.sidebar.button('Reinitialize Database'):
    logger.info("Reinitializing database...")
    drop_tables()
    init_db()
    st.sidebar.success('Database reinitialized.')
    schema = print_schema()
    logger.info(f"Database schema after reinitialization: {schema}")
    st.sidebar.text(f'Current schema:\n{schema}')

if st.button('Fetch and Analyze Data'):
    logger.info(f"Fetching and analyzing data for {ticker_symbol}")
    try:
        # Obtener datos financieros
        financial_data = get_financial_data(ticker_symbol)
        
        if financial_data.empty:
            logger.warning(f"No financial data available for {ticker_symbol}")
            st.error(f"No se pudieron obtener datos financieros para {ticker_symbol}. Por favor, verifica el símbolo del ticker.")
        else:
            logger.info(f"Successfully fetched data for {ticker_symbol}")
            # Insertar datos en la base de datos
            insert_financial_data(financial_data, ticker_symbol)
            
            # Mostrar los datos
            st.write(f"Financial data for {ticker_symbol}:")
            st.dataframe(financial_data)
            
            # Agregar más análisis y visualizaciones aquí
            if 'Total Revenue' in financial_data.columns:
                st.line_chart(financial_data['Total Revenue'])
                logger.info("Displayed Total Revenue chart")
            if 'Net Margin %' in financial_data.columns:
                st.line_chart(financial_data['Net Margin %'])
                logger.info("Displayed Net Margin % chart")
    except Exception as e:
        logger.error(f"An error occurred while processing {ticker_symbol}: {str(e)}", exc_info=True)
        st.error(f"An error occurred: {str(e)}")

# Función para mostrar datos históricos
def show_historical_data():
    logger.info("Fetching historical data")
    session = Session(bind=engine)
    data = session.query(FinancialData).all()
    df = pd.DataFrame([vars(d) for d in data])
    session.close()
    
    st.write("Historical Financial Data:")
    st.dataframe(df)
    logger.info(f"Displayed historical data. Shape: {df.shape}")

if st.button('Show Historical Data'):
    show_historical_data()