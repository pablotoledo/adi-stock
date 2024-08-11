import yfinance as yf
import pandas as pd
import numpy as np
import json
from utils.logger import logger

class NpEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        if isinstance(obj, np.floating):
            return float(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        if isinstance(obj, (pd.Timestamp, pd.Period)):
            return obj.isoformat()
        if pd.isna(obj) or np.isnan(obj):
            return None
        return super(NpEncoder, self).default(obj)

def get_financial_data(ticker_symbol):
    logger.info(f"Fetching data for {ticker_symbol}")
    company = yf.Ticker(ticker_symbol)
    
    # Obtener datos financieros
    income_stmt = company.income_stmt
    balance_sheet = company.balance_sheet
    cash_flow = company.cash_flow

    if income_stmt.empty and balance_sheet.empty and cash_flow.empty:
        logger.warning(f"No financial data available for {ticker_symbol}")
        return pd.DataFrame()

    # Combinar todos los datos financieros
    all_data = pd.concat([income_stmt, balance_sheet, cash_flow], axis=0)
    all_data = all_data.transpose()

    # Asegurarse de que el índice sea de tipo datetime
    all_data.index = pd.to_datetime(all_data.index)

    # Convertir a numérico, ignorando errores
    all_data = all_data.apply(pd.to_numeric, errors='coerce')

    # Calcular algunas métricas adicionales comunes
    if 'Total Revenue' in all_data.columns:
        all_data['Y/Y Growth %'] = all_data['Total Revenue'].pct_change() * 100
        if 'Net Income' in all_data.columns:
            all_data['Net Margin %'] = (all_data['Net Income'] / all_data['Total Revenue']) * 100
        if 'Gross Profit' in all_data.columns:
            all_data['Gross Margin %'] = (all_data['Gross Profit'] / all_data['Total Revenue']) * 100
    if 'EBITDA' in all_data.columns and 'Total Revenue' in all_data.columns:
        all_data['EBITDA Margin %'] = (all_data['EBITDA'] / all_data['Total Revenue']) * 100
    if 'Operating Income' in all_data.columns and 'Total Revenue' in all_data.columns:
        all_data['Operating Margin %'] = (all_data['Operating Income'] / all_data['Total Revenue']) * 100
    if 'Income Tax Expense' in all_data.columns and 'Income Before Tax' in all_data.columns:
        all_data['Tax Rate %'] = (all_data['Income Tax Expense'] / all_data['Income Before Tax']) * 100

    # Reemplazar inf y -inf con None, pero mantener 0
    all_data = all_data.replace([np.inf, -np.inf], np.nan)
    all_data = all_data.where(pd.notnull(all_data) | (all_data == 0), None)

    # Ordenar por fecha
    all_data = all_data.sort_index()

    logger.info(f"Processed data columns: {all_data.columns}")
    logger.info(f"Data shape: {all_data.shape}")
    logger.debug(f"Processed financial data:\n{all_data}")
    
    return all_data

def load_historical_data(ticker_symbol):
    logger.info(f"Loading historical data for {ticker_symbol}")
    try:
        # Obtener datos financieros
        financial_data = get_financial_data(ticker_symbol)
        
        if financial_data.empty:
            logger.warning(f"No historical data available for {ticker_symbol}")
            return None
        
        # Función para buscar columnas con nombres similares
        def find_column(df, possible_names):
            for name in possible_names:
                if name in df.columns:
                    return df[name]
            logger.warning(f"Columns not found. Possible names: {possible_names}")
            return pd.Series(index=df.index, dtype='float64')  # Retorna una serie vacía si no se encuentra

        # Seleccionar y renombrar las columnas relevantes para el modelo de valoración
        historical_data = pd.DataFrame({
            'Ventas': find_column(financial_data, ['Total Revenue', 'Revenue']),
            'Beneficio Operativo': find_column(financial_data, ['Operating Income', 'EBIT']),
            'Depreciación y Amortización': find_column(financial_data, ['Depreciation & Amortization', 'Depreciation And Amortization', 'Depreciation']),
            'Intereses': find_column(financial_data, ['Interest Expense', 'Interest Paid']),
            'Impuestos': find_column(financial_data, ['Income Tax Expense', 'Tax Provision']),
            'Número de Acciones': find_column(financial_data, ['Diluted Average Shares', 'Basic Average Shares'])
        })
        
        # Convertir los datos a millones (si es necesario)
        for column in historical_data.columns:
            if column != 'Número de Acciones':
                historical_data[column] = historical_data[column] / 1e6
        
        # Ordenar por fecha y seleccionar los últimos 7 años
        historical_data = historical_data.sort_index(ascending=False).head(7)
        
        # Añadir la columna de Año
        historical_data['Año'] = historical_data.index.year
        
        logger.info(f"Successfully loaded historical data for {ticker_symbol}")
        logger.debug(f"Loaded data:\n{historical_data}")
        return historical_data
    
    except Exception as e:
        logger.error(f"Error loading historical data for {ticker_symbol}: {str(e)}", exc_info=True)
        return None