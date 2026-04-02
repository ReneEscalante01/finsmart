from pydantic import BaseModel
from typing import Optional

class PrediccionResponse(BaseModel):
    prediccion: Optional[float] = None
    mensaje: str
    
class AnomaliasResponse(BaseModel):
    anomalia: Optional[bool] = None
    mensaje: str
    
class ConsejosResponse(BaseModel):
    mensaje: Optional[str] = None
    consejo: str
    
class AlertaPresupuestoResponse(BaseModel):
    categoria_id: str
    mensaje: str