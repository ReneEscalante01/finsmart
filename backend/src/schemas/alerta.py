from pydantic import BaseModel, field_validator
from uuid import UUID
from datetime import datetime
from typing import Optional

class AlertaBase(BaseModel):
    tipo_alerta: str
    mensaje: str
    valor_detectado: Optional[float] = None
    leida: bool = False
    
    @field_validator("tipo_alerta", "mensaje")
    @classmethod
    def vacio(cls, v):
        if v is not None and v.strip() == "":
            raise ValueError("El campo no puede estar vacio")
        return v

class AlertaUpdate(BaseModel):
    leida: Optional[bool] = None
    
class AlertaResponse(AlertaBase):
    id: UUID
    usuario_id: UUID
    generada_en: datetime

    
    class Config: 
        from_attributes = True
        
class AlertaResponseModel(BaseModel):
    message: str
    data: Optional[AlertaResponse] = None
    
    class Config:
        from_attributes = True