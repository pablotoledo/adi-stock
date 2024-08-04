from sqlalchemy.orm import Session
from models import FinancialData, engine
import json
from finance_data import NpEncoder
from utils.logger import logger

def insert_financial_data(financial_data, ticker_symbol):
    logger.info(f"Inserting financial data for {ticker_symbol}")
    session = Session(bind=engine)
    
    for date, data in financial_data.iterrows():
        logger.debug(f"Processing data for date: {date}")
        json_data = json.dumps(data.to_dict(), cls=NpEncoder)
        logger.debug(f"JSON data: {json_data}")
        financial_entry = FinancialData(
            ticker=ticker_symbol,
            date=date,
            data=json.loads(json_data)  # Convertir de nuevo a dict después de la serialización
        )
        
        session.merge(financial_entry)
    
    try:
        session.commit()
        logger.info(f"Successfully inserted/updated data for {ticker_symbol}")
    except Exception as e:
        session.rollback()
        logger.error(f"Error inserting data for {ticker_symbol}: {str(e)}", exc_info=True)
    finally:
        session.close()