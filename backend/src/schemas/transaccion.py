from pydantic import BaseModel
from uuid import UUID
from datetime import datetime 
from typing import Optional

class TransaccionBase(BaseModel):
    monto: float
    tipo: str
    nota: Optional[str] = None
    fecha: datetime
    
class TransaccionCreate(TransaccionBase):
    usuario_id: UUID
    cuenta_id: UUID
    categoria_id: UUID
    
class TransaccionResponse(TransaccionBase):
    id: UUID
    usuario_id: UUID
    cuenta_id: UUID
    categoria_id: UUID
    fecha_creacion: datetime
    
    class Config:
        from_attributes = True