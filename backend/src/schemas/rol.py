from pydantic import BaseModel, field_validator
from typing import Optional

class RolBase(BaseModel):
    nombre_rol: str
    
    @field_validator("nombre_rol")
    @classmethod
    def vacio(cls, v):
        if v is not None and v.strip() == "":
            raise ValueError("El campo no puede estar vacio")
        return v

class RolCreate(RolBase):
    pass
    
class RolUpdate(BaseModel):
    nombre: Optional[str] = None
    
    @field_validator("nombre")
    @classmethod
    def vacio(cls, v):
        if v is not None and v.strip() == "":
            raise ValueError("El campo no puede estar vacio")
        return v

class RolResponse(RolBase):
    id: int
    
    class Config:
        from_attributes = True

class RolResponseModel(BaseModel):
    message: str
    data: Optional[RolResponse] = None
    
    class Config:
        from_attributes = True