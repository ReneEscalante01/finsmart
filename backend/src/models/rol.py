from sqlalchemy import Column, String, Integer
from src.database import Base

class Rol(Base):
    __tablename__ = "roles"
    
    id = Column(Integer, primary_key=True)
    nombre_rol = Column(String(20), nullable=False)