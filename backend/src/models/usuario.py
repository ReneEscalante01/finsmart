from sqlalchemy import Column, String, TIMESTAMP
from sqlalchemy.dialects.postgresql import UUID
import uuid
from sqlalchemy.sql import func
from src.database import Base

class Usuario(Base):
    __tablename__ = "usuarios"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nombre = Column(String(150), nullable=False)
    email = Column(String(100), nullable=False)
    contrasena_hash = Column(String(250), nullable=False)
    moneda = Column(String(10), default="MXN")
    fecha_creacion = Column(TIMESTAMP, server_default=func.now())