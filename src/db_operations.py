from sqlalchemy.orm import Session
from models import FinancialData, engine
import logging

def insert_financial_data(financial_data, ticker_symbol):
    session = Session(bind=engine)
    
    for date, data in financial_data.iterrows():
        financial_entry = FinancialData(
            ticker=ticker_symbol,
            date=date,
            total_revenue=data.get('Sales'),
            ebitda=data.get('EBITDA'),
            ebit=data.get('EBIT'),
            interest_expense=data.get('Interest Expense'),
            pretax_income=data.get('Pretax Income'),
            income_taxes=data.get('Income Taxes'),
            net_income=data.get('Net Income'),
            diluted_eps=data.get('Diluted EPS'),
            diluted_average_shares=data.get('Diluted Average Shares'),
            yoy_growth=data.get('Y/Y Growth %'),
            ebitda_margin=data.get('EBITDA Margin %'),
            ebit_margin=data.get('EBIT Margin %'),
            tax_rate=data.get('Tax Rate'),
            net_margin=data.get('Net Margin %')
        )
        
        session.merge(financial_entry)
    
    try:
        session.commit()
        logging.info(f"Successfully inserted/updated data for {ticker_symbol}")
    except Exception as e:
        session.rollback()
        logging.error(f"Error inserting data for {ticker_symbol}: {str(e)}")
    finally:
        session.close()