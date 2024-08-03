import yfinance as yf
import pandas as pd
import numpy as np
import logging

logging.basicConfig(level=logging.INFO)

def get_financial_data(ticker_symbol):
    logging.info(f"Fetching data for {ticker_symbol}")
    company = yf.Ticker(ticker_symbol)
    
    financials = company.financials
    if financials.empty:
        logging.warning(f"No financial data available for {ticker_symbol}")
        return pd.DataFrame()

    financials = financials.transpose()
    logging.info(f"Raw financial data columns: {financials.columns}")
    financials.fillna(value=np.nan, inplace=True)

    # Definir un mapeo flexible de nombres de columnas
    column_mapping = {
        'Sales': ['Total Revenue', 'Revenue', 'Sales', 'Operating Revenue'],
        'EBITDA': ['EBITDA', 'Normalized EBITDA'],
        'EBIT': ['EBIT', 'Operating Income'],
        'Interest Expense': ['Interest Expense'],
        'Pretax Income': ['Pretax Income', 'Income Before Tax'],
        'Income Taxes': ['Income Tax Expense', 'Tax Provision'],
        'Net Income': ['Net Income', 'Net Income Common Stockholders'],
        'Diluted EPS': ['Diluted EPS'],
        'Diluted Average Shares': ['Diluted Average Shares']
    }

    df = pd.DataFrame(index=financials.index[:10])

    # Función auxiliar para obtener el valor de una columna con múltiples nombres posibles
    def get_column_value(data, possible_names):
        for name in possible_names:
            if name in data.columns:
                return data[name]
        logging.warning(f"Could not find any matching column for {possible_names}")
        return pd.Series([np.nan] * len(data), index=data.index)

    # Llenar el DataFrame con los valores disponibles
    for col, possible_names in column_mapping.items():
        df[col] = get_column_value(financials, possible_names)

    # Convertir a numérico, ignorando errores
    df = df.apply(pd.to_numeric, errors='coerce')

    # Calcular métricas adicionales
    if 'Sales' in df.columns and not df['Sales'].isnull().all():
        df['Y/Y Growth %'] = df['Sales'].pct_change() * 100
        if 'EBITDA' in df.columns:
            df['EBITDA Margin %'] = (df['EBITDA'] / df['Sales']) * 100
        if 'EBIT' in df.columns:
            df['EBIT Margin %'] = (df['EBIT'] / df['Sales']) * 100
        if 'Net Income' in df.columns:
            df['Net Margin %'] = (df['Net Income'] / df['Sales']) * 100
    if 'Pretax Income' in df.columns and 'Income Taxes' in df.columns:
        df['Tax Rate'] = (df['Income Taxes'] / df['Pretax Income']) * 100

    # Reemplazar NaN con None para que SQLAlchemy maneje correctamente estos valores
    df = df.where(pd.notnull(df), None)

    logging.info(f"Processed data columns: {df.columns}")
    logging.info(f"Data shape: {df.shape}")

    return df