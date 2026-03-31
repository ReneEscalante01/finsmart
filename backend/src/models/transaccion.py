from sqlalchemy import Column, ForeignKey, Float, String, DATE, TIMESTAMP
from sqlalchemy.dialects.postgresql import UUID
import uuid
from sqlalchemy.sql import func
from src.database import Base

class Transaccion(Base):
    __tablename__ = "transacciones"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    usuario_id = Column(UUID(as_uuid=True), ForeignKey("usuarios.id", ondelete="CASCADE"), nullable=False)
    cuenta_id = Column(UUID(as_uuid=True), ForeignKey("cuentas.id", ondelete="CASCADE"), nullable=False)
    categoria_id = Column(UUID(as_uuid=True), ForeignKey("categoria.id", ondelete="CASCADE"), nullable=False)
    monto = Column(Float, nullable=False)
    tipo = Column(String(50), nullable=False)
    nota = Column(String(100))
    fecha = Column(DATE, nullable=False)
    fecha_creacion = Column(TIMESTAMP, server_default=func.now())
    