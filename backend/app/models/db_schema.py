from sqlalchemy import create_engine, Column, Integer, String, TIMESTAMP, Text, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime
import pytz

DB_URL = "mysql+pymysql://root:2005@localhost/quote"

engine = create_engine(DB_URL)

Base = declarative_base()

IST = pytz.timezone('Asia/Kolkata')

class User(Base):
    __tablename__ = "user_table"
    id = Column(Integer, primary_key=True)
    email = Column(String(100), nullable=False, unique=True)
    created_at = Column(TIMESTAMP, default=datetime.now)
    name  = Column(String(100))
    sent_quotes = relationship("SentQuote", back_populates="user")
    
class Quotes(Base):
    __tablename__ = "quotes_table"
    id = Column(Integer, primary_key=True)
    content = Column(Text, nullable=False)
    author = Column(String(50))
    created_at = Column(TIMESTAMP, default=datetime.now)
    sent_quotes = relationship("SentQuote", back_populates="quote")  # Define the relationship after both classes are defined

class SentQuote(Base):
    __tablename__ = 'sent_quotes'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user_table.id'), nullable=False)
    quote_id = Column(Integer, ForeignKey('quotes_table.id'), nullable=False)
    sent_at = Column(TIMESTAMP, default=datetime.now)
    user = relationship("User", back_populates="sent_quotes")
    quote = relationship("Quotes", back_populates="sent_quotes")

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)