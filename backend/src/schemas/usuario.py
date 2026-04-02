from pydantic import BaseModel, EmailStr, field_validator
from uuid import UUID
from datetime import datetime
from typing import Optional

class UsuarioBase(BaseModel):
    nombre: str
    email: EmailStr
    moneda: str = "MXN"
    
    @field_validator("nombre", "email", "moneda")
    @classmethod
    def vacio(cls, v):
        if v is not None and v.strip() == "":
            raise ValueError("El campo no puede estar vacio")
        return v
    
class UsuarioCreate(UsuarioBase):
    rol_id: int
    contrasena: str

    
class UsuarioUpdate(BaseModel): 
    nombre: Optional[str] = None
    email: Optional[EmailStr] = None
    moneda: Optional[str] = None
    contrasena: Optional[str] = None
    
    @field_validator("nombre", "email", "moneda")
    @classmethod
    def vacio(cls, v):
        if v is not None and v.strip() == "":
            raise ValueError("El campo no puede estar vacio")
        return v
    
class UsuarioResponse(UsuarioBase):
    id: UUID
    rol_id: int
    fecha_creacion: datetime
    
    class Config:
        from_attributes = True
        
class UsuarioResponseModel(BaseModel):
    message: str
    data: Optional[UsuarioResponse] = None
    
    class Config: 
        from_attributes = True
        