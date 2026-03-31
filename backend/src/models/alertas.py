from sqlalchemy import Column, ForeignKey, Boolean, TIMESTAMP, Float, String, Text
from sqlalchemy.dialects.postgresql import UUID
import uuid
from sqlalchemy.sql import func
from src.database import Base

class Alerta(Base):
    __tablename__ = "alertas_ml"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    usuario_id = Column(UUID(as_uuid=True), ForeignKey("usuarios.id", ondelete="CASCADE"), nullable=False)
    tipo_alerta = Column(String(50), nullable=False)
    mensaje = Column(Text, nullable=False)
    valor_detectado = Column(Float)
    leida = Column(Boolean, default=False)
    generada_en = Column(TIMESTAMP, server_default=func.now())
    