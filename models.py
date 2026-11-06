from sqlalchemy import Column, Integer, String, DateTime
from database import Base
import datetime
from sqlalchemy import Column, Integer, String
from database import Base

class Stock(Base):
    __tablename__ = "stocks"
    
    id = Column(Integer, primary_key=True, index=True)
    item = Column(String, unique=True, index=True)
    quantity = Column(Integer, default=0)

class Material(Base):
    __tablename__ = "materials"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)  
    quantity = Column(Integer, default=0)          

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)  
    quantity = Column(Integer, default=0)          

class ProductionLog(Base):
    __tablename__ = "production_logs"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    action = Column(String)
    status = Column(String)                        