from sqlalchemy import Column, String, ForeignKey, TIMESTAMP, Float
from sqlalchemy.dialects.postgresql import UUID
import uuid
from sqlalchemy.sql import func
from src.database import Base

class Cuenta(Base):
    __tablename__ = "cuentas"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    usuario_id = Column(UUID(as_uuid=True), ForeignKey("usuarios.id", ondelete="CASCADE"), nullable=False)
    nombre = Column(String(50), nullable=False)
    tipo = Column(String(50), nullable=False)
    saldo_inicial = Column(Float, default=0)
    saldo_actual = Column(Float, default=0)
    fecha_creacion = Column(TIMESTAMP, server_default=func.now())