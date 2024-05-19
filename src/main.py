import os
import django
from finance.finance_data import get_financial_data
from db.db_operations import insert_financial_data
from utils.logger import setup_logger

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()

def main():
    logger = setup_logger()
    
    ticker_symbol = 'MCD'  # McDonald's Corporation
    logger.info(f"Fetching financial data for {ticker_symbol}")
    
    financial_data = get_financial_data(ticker_symbol)
    
    insert_financial_data(financial_data, ticker_symbol)
    logger.info("Data insertion completed successfully")

if __name__ == "__main__":
    main()
