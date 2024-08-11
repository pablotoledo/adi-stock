import streamlit as st
import pandas as pd
from sqlalchemy.orm import Session
from models import FinancialData, engine, init_db, print_schema, drop_tables
from finance_data import get_financial_data, load_historical_data
from db_operations import insert_financial_data
from utils.logger import logger
import plotly.express as px

# Importar las nuevas funciones
from historical_data_input import historical_data_input
from future_projections import future_projections
from valuation_calculations import calculate_valuation, calculate_intrinsic_value
from valuation_visualizations import plot_historical_and_projected_data, plot_valuation_metrics

# Inicializar la base de datos
init_db()
logger.info("Database initialized")

def main():
    st.title('Financial Data Analyzer and Valuation Model')

    # Sidebar
    st.sidebar.title("Opciones")
    
    if st.sidebar.button('Reinitialize Database'):
        logger.info("Reinitializing database...")
        drop_tables()
        init_db()
        st.sidebar.success('Database reinitialized.')
        schema = print_schema()
        logger.info(f"Database schema after reinitialization: {schema}")
        st.sidebar.text(f'Current schema:\n{schema}')

    # Input para el símbolo del ticker
    ticker_symbol = st.sidebar.text_input('Enter a ticker symbol (e.g., META for Meta/Facebook):', 'META')

    # Crear pestañas
    tabs = st.tabs(["Obtener Datos", "Datos Históricos", "Proyecciones", "Valoración"])

    with tabs[0]:
        st.header("Obtener Datos Financieros")
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

    with tabs[1]:
        st.header("Datos Históricos")
        # Cargar datos históricos automáticamente
        historical_data = load_historical_data(ticker_symbol)
        
        # Mostrar los datos históricos cargados automáticamente
        if historical_data is not None and not historical_data.empty:
            st.write("Datos históricos cargados automáticamente:")
            st.dataframe(historical_data)
            
            # Opción para editar los datos
            if st.checkbox("Editar datos históricos"):
                edited_data = st.data_editor(historical_data)
                if st.button("Guardar cambios"):
                    historical_data = edited_data
                    st.success("Cambios guardados exitosamente")
        else:
            st.warning("No se pudieron cargar datos históricos automáticamente. Por favor, ingrese los datos manualmente.")
            historical_data = historical_data_input()
            
    with tabs[2]:
        st.header("Proyecciones Futuras")
        years, growth_rate, operating_margin, tax_rate = future_projections()

    with tabs[3]:
        st.header("Valoración")
        if st.button("Calcular Valoración"):
            if historical_data is not None and not historical_data.empty:
                projections = calculate_valuation(historical_data, years, growth_rate, operating_margin, tax_rate)
                st.write("Proyecciones:")
                st.dataframe(projections)

                intrinsic_value = calculate_intrinsic_value(projections)
                st.write(f"Valor Intrínseco Estimado: ${intrinsic_value:,.2f}")

                plot_historical_and_projected_data(historical_data, projections)
                plot_valuation_metrics(historical_data, projections)
            else:
                st.warning("Por favor, ingrese los datos históricos antes de calcular la valoración.")

    # Botón para mostrar datos históricos (mantenido de la versión anterior)
    if st.sidebar.button('Show Historical Data'):
        show_historical_data()

def show_historical_data():
    logger.info("Fetching historical data")
    session = Session(bind=engine)
    data = session.query(FinancialData).all()
    df = pd.DataFrame([vars(d) for d in data])
    session.close()
    
    st.write("Historical Financial Data:")
    st.dataframe(df)
    logger.info(f"Displayed historical data. Shape: {df.shape}")

if __name__ == "__main__":
    main()