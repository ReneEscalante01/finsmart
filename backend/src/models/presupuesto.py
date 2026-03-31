from sqlalchemy import Column, ForeignKey, String, DATE, Float
from sqlalchemy.dialects.postgresql import UUID
import uuid
from src.database import Base

class Presupuesto(Base):
    __tablename__ = "presupuestos"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    usuario_id = Column(UUID(as_uuid=True), ForeignKey("usuarios.id", ondelete="CASCADE"), nullable=False)
    categoria_id = Column(UUID(as_uuid=True), ForeignKey("categorias.id", ondelete="CASCADE"), nullable=False)
    monto_limite = Column(Float, nullable=False)
    periodo = Column(String(20), nullable=False)
    fecha_inicio = Column(DATE, nullable=False)
    fecha_fin = Column(DATE, nullable=False)