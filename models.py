from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class TurtleSoup(Base):
    __tablename__ = 'turtle-soup-db' 
    id = Column(Integer, primary_key=True)
    title = Column(String)