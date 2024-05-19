import os

# Configurar el entorno de Django antes de cualquier otra importación
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.mysite.settings')

import django
django.setup()

from finance_data import get_financial_data
from db_operations import insert_financial_data
from utils.logger import setup_logger

def main():
    # Seleccionar la base de datos
    database = os.getenv('DJANGO_DATABASE', 'default')
    from django.conf import settings
    if database == 'local':
        settings.DATABASES['default'].update(settings.DATABASES['local'])

    logger = setup_logger()
    
    ticker_symbol = 'MCD'  # McDonald's Corporation
    logger.info(f"Fetching financial data for {ticker_symbol}")
    
    financial_data = get_financial_data(ticker_symbol)
    
    insert_financial_data(financial_data, ticker_symbol)
    logger.info("Data insertion completed successfully")

if __name__ == "__main__":
    main()
