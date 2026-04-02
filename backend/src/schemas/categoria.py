from pydantic import BaseModel, field_validator
from uuid import UUID
from typing import Optional

class CategoriaBase(BaseModel):
    nombre: str
    icono: Optional[str] = None
    color: Optional[str] = None
    es_default: bool = False
    usuario_id: Optional[UUID] = None
    
    @field_validator("nombre")
    @classmethod 
    def vacio(cls, v):
        if v is not None and v.strip() == "":
            raise ValueError("El campo no puede estar vacio")
        return v
    
class CategoriaCreate(CategoriaBase):
    pass

class CategoriaUpdate(BaseModel):
    nombre: Optional[str] = None
    icono: Optional[str] = None
    color: Optional[str] = None
    es_default: Optional[bool] = None
    
    @field_validator("nombre", "icono", "color")
    @classmethod
    def vacio(cls, v):
        if v is not None and v.strip() == "":
            raise ValueError("El campo no puede estar vacio")
        return v
    
    
class CategoriaResponse(CategoriaBase):
    id: UUID
    usuario_id: Optional[UUID] = None
        
    class Config:
        from_attributes = True
        
class CategoriaResponseModel(BaseModel):
    message: str
    data: Optional[CategoriaResponse] = None
    
    class Config:
        from_attributes = True