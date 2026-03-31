from pydantic import BaseModel
from uuid import UUID
from datetime import datetime

class PresupuestoBase(BaseModel):
    periodo: str
    monto_limite: float
    fecha_inicio: datetime
    fecha_fin: datetime
    
class PresupuestoCreate(PresupuestoBase):
    usuario_id: UUID
    categoria_id: UUID
        
class PresupuestoResponse(PresupuestoBase):
    id: UUID
    usuario_id: UUID
    categoria_id: UUID
    
    class Config:
        from_attributes = True