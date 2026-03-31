from pydantic import BaseModel
from uuid import UUID 
from datetime import datetime

class CuentaBase(BaseModel):
    nombre: str
    tipo: str
    saldo_inicial: float = 0
    saldo_actual: float = 0
        
class CuentaCreate(CuentaBase):
    usuario_id = UUID
    
class CuentaResponse(CuentaBase):
    id: UUID
    usuario_id = UUID
    fecha_creacion: datetime
    
    class Config:
        from_attributes = True