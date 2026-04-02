from pydantic import BaseModel, field_validator
from uuid import UUID 
from datetime import datetime
from typing import Optional, Literal

class CuentaBase(BaseModel):
    nombre: str
    tipo: Literal["efectivo", "debito", "credito", "ahorro"]
    saldo_inicial: float = 0
    saldo_actual: float = 0
    
    @field_validator("nombre")
    @classmethod
    def vacio(cls, v):
        if v is not None and v.strip() == "":
            raise ValueError("El campo no puede estar vacio")
        return v
    
        
class CuentaCreate(CuentaBase):
    pass
    
class CuentaUpdate(BaseModel):
    nombre: Optional[str] = None
    tipo: Optional[Literal["efectivo", "debito", "credito", "ahorro"]] = None
        
    @field_validator("nombre")
    @classmethod
    def vacio(cls, v):
        if v is not None and v.strip() == "":
            raise ValueError("El campo no puede estar vacio")
        return v
    
    
class CuentaResponse(CuentaBase):
    id: UUID
    usuario_id: UUID
    fecha_creacion: datetime
    
    class Config:
        from_attributes = True
        
class CuentaResponseModel(BaseModel):
    message: str
    data: Optional[CuentaResponse] = None
    
    class Config:
        from_attributes = True
        