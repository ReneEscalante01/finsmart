from pydantic import BaseModel, EmailStr
from uuid import UUID
from datetime import datetime

class UsuarioBase(BaseModel):
    nombre: str
    email: EmailStr
    moneda: str = "MXN"
    
class UsuarioCreate(UsuarioBase):
    contrasena: str
    
class UsuarioResponse(UsuarioBase):
    id: UUID
    fecha_creacion: datetime
    
    class Config:
        from_attributes = True