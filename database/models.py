from sqlalchemy import Column, Integer, String, Float, Date
from database.connection import Base

class MacroIndicator(Base):
    __tablename__ = "macro_indicators"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, index=True)
    country = Column(String(50), index=True)
    region = Column(String(50), index=True)
    inflation_rate = Column(Float)
    gdp_growth = Column(Float)
    unemployment_rate = Column(Float)

class ConsumerInsight(Base):
    __tablename__ = "consumer_insights"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, index=True)
    country = Column(String(50), index=True)
    region = Column(String(50), index=True)
    consumer_spending_index = Column(Float)
    digital_payment_adoption = Column(Float)
