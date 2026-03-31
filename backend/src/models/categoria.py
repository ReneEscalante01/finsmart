from sqlalchemy import Column, String, Boolean
from sqlalchemy.dialects.postgresql import UUID
import uuid
from src.database import Base

class Categoria(Base):
    __tablename__ = "categorias"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nombre = Column(String(50), nullable=False)
    icono = Column(String(50))
    color = Column(String(30))
    es_default = Column(Boolean, default=False)