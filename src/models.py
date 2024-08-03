from sqlalchemy import create_engine, Column, Integer, String, Date, Numeric
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class FinancialData(Base):
    __tablename__ = 'financial_data'

    id = Column(Integer, primary_key=True)
    ticker = Column(String(10))
    date = Column(Date)
    total_revenue = Column(Numeric(20, 2))
    ebitda = Column(Numeric(20, 2))
    ebit = Column(Numeric(20, 2))
    interest_expense = Column(Numeric(20, 2))
    pretax_income = Column(Numeric(20, 2))
    income_taxes = Column(Numeric(20, 2))
    net_income = Column(Numeric(20, 2))
    diluted_eps = Column(Numeric(10, 2))
    diluted_average_shares = Column(Numeric(20, 2))
    yoy_growth = Column(Numeric(5, 2))
    ebitda_margin = Column(Numeric(5, 2))
    ebit_margin = Column(Numeric(5, 2))
    tax_rate = Column(Numeric(5, 2))
    net_margin = Column(Numeric(5, 2))

# Configuración de la base de datos
#engine = create_engine('postgresql://your_username:your_password@db/financials')

engine = create_engine('postgresql://your_username:your_password@localhost/financials')
Session = sessionmaker(bind=engine)

def init_db():
    Base.metadata.create_all(engine)
