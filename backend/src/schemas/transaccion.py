from pydantic import BaseModel
from uuid import UUID
from datetime import datetime 
from typing import Optional, Literal 

class TransaccionBase(BaseModel):
    monto: float
    tipo: Literal["gasto", "ingreso"]
    nota: Optional[str] = None
    fecha: datetime
    
class TransaccionCreate(TransaccionBase):
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

class TransaccionResponseModel(BaseModel):
    message: str
    data: Optional[TransaccionResponse] = None
    
    class Config:
        from_attributes = True