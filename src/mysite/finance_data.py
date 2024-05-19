import yfinance as yf
import pandas as pd
import numpy as np

def get_financial_data(ticker_symbol):
    company = yf.Ticker(ticker_symbol)
    financials = company.financials.transpose()
    financials.fillna(value=np.nan, inplace=True)  # Reemplaza 'None' por NaN para cálculos

    df = pd.DataFrame(index=financials.index[:10])

    financials = financials.apply(pd.to_numeric, errors='coerce')

    df['Sales'] = financials['Total Revenue']
    df['EBITDA'] = financials['EBITDA']
    df['EBIT'] = financials['EBIT']
    df['Interest Expense'] = financials['Interest Expense']
    df['Pretax Income'] = financials['Pretax Income']
    df['Income Taxes'] = financials['Tax Provision']
    df['Consolidated Net Income'] = financials['Net Income']
    df['Diluted EPS'] = financials['Diluted EPS']
    df['Diluted Average Shares'] = financials['Diluted Average Shares']

    df['Y/Y Growth %'] = df['Sales'].pct_change() * 100
    df['EBITDA Margin %'] = (df['EBITDA'] / df['Sales']) * 100
    df['EBIT Margin %'] = (df['EBIT'] / df['Sales']) * 100
    df['Tax Rate'] = (df['Income Taxes'] / df['Pretax Income']) * 100
    df['Net Margin %'] = (df['Consolidated Net Income'] / df['Sales']) * 100

    # Reemplazar NaN con None para que Django maneje correctamente estos valores
    df = df.where(pd.notnull(df), None)

    df = df.astype(object).where(pd.notnull(df), None)

    return df
