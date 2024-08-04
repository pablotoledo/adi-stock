from sqlalchemy import create_engine, Column, Integer, String, Date, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import inspect
from utils.logger import logger

Base = declarative_base()

class FinancialData(Base):
    __tablename__ = 'financial_data'

    id = Column(Integer, primary_key=True)
    ticker = Column(String(10), index=True)
    date = Column(Date, index=True)
    data = Column(JSON)  # This will store all financial metrics as a JSON object

engine = create_engine('postgresql://your_username:your_password@localhost/financials')
Session = sessionmaker(bind=engine)

def drop_tables():
    logger.info("Dropping all tables")
    Base.metadata.drop_all(engine)

def print_schema():
    logger.info("Printing database schema")
    inspector = inspect(engine)
    schema = []
    for table_name in inspector.get_table_names():
        for column in inspector.get_columns(table_name):
            schema.append(f"Table: {table_name}, Column: {column['name']}, Type: {column['type']}")
    return "\n".join(schema)

def init_db():
    logger.info("Initializing database")
    Base.metadata.create_all(engine)
    logger.info("Database initialized successfully")