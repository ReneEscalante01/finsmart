from pydantic import BaseModel
from uuid import UUID
from typing import Optional

class CategoriaBase(BaseModel):
    nombre: str
    icono: Optional[str] = None
    color: Optional[str] = None
    es_default: bool = False
    
class CategoriaCreate(CategoriaBase):
    pass
    
class CategoriaResponse(CategoriaBase):
    id: UUID
        
    class Config:
        from_attributes = True
