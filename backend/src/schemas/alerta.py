from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from typing import Optional

class AlertaBase(BaseModel):
    tipo_alerta: str
    mensaje: str
    valor_detectado: Optional[float] = None
    leida: bool = False
    
class AlertaCreate(AlertaBase):
    usuario_id: UUID
    
class AlertaResponse(AlertaBase):
    id: UUID
    usuario_id: UUID
    generada_en: datetime

    
    class Config: 
        from_attributes = True