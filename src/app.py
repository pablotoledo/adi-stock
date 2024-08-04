import streamlit as st
import pandas as pd
from sqlalchemy.orm import Session
from models import FinancialData, engine, init_db, print_schema, drop_tables
from finance_data import get_financial_data
from db_operations import insert_financial_data
from utils.logger import logger
import plotly.express as px

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
        
        if not financial_data.empty:
            # Mostrar los datos
            st.write(f"Financial data for {ticker_symbol}:")
            st.dataframe(financial_data)
            
            # Preparar datos para gráficos
            financial_data.index = pd.to_datetime(financial_data.index)
            financial_data = financial_data.sort_index()

            # Gráfico de Total Revenue
            if 'Total Revenue' in financial_data.columns:
                fig_revenue = px.line(financial_data, x=financial_data.index, y='Total Revenue', 
                                      title=f'{ticker_symbol} Total Revenue Over Time')
                fig_revenue.update_xaxes(title='Date')
                fig_revenue.update_yaxes(title='Total Revenue (USD)', tickformat=',.0f')
                st.plotly_chart(fig_revenue)
                logger.info("Displayed Total Revenue chart")

            # Gráfico de Net Margin %
            if 'Net Margin %' in financial_data.columns:
                fig_margin = px.line(financial_data, x=financial_data.index, y='Net Margin %', 
                                     title=f'{ticker_symbol} Net Margin % Over Time')
                fig_margin.update_xaxes(title='Date')
                fig_margin.update_yaxes(title='Net Margin %', tickformat='.2f')
                st.plotly_chart(fig_margin)
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