from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from typing import Optional, Literal

class PresupuestoBase(BaseModel):
    periodo: Literal["semanal", "mensual"]
    monto_limite: float
    fecha_inicio: datetime
    fecha_fin: datetime
    
class PresupuestoCreate(PresupuestoBase):
    categoria_id: UUID

class PresupuestoUpdate(BaseModel):
    monto_limite: Optional[float] = None
    fecha_fin: Optional[datetime] = None
    periodo: Optional[Literal["semanal", "mensual"]] = None
        
class PresupuestoResponse(PresupuestoBase):
    id: UUID
    usuario_id: UUID
    categoria_id: UUID
    
    class Config:
        from_attributes = True

class PresupuestoResponseModel(BaseModel):
    message: str
    data: Optional[PresupuestoResponse] = None
    
    class Config:
        from_attributes = True