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

    logger.info(f"Raw financial data columns: {all_data.columns}")
    logger.debug(f"Raw financial data:\n{all_data}")

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

    # Reemplazar NaN e inf con None
    all_data = all_data.replace([np.inf, -np.inf, np.nan], None)
    all_data = all_data.where(pd.notnull(all_data), None)

    logger.info(f"Processed data columns: {all_data.columns}")
    logger.info(f"Data shape: {all_data.shape}")
    logger.debug(f"Processed financial data:\n{all_data}")
    
    return all_data