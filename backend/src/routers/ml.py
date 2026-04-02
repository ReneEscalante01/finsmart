from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.database import get_db
from src.models.alerta import Alerta
from src.schemas.ml import PrediccionResponse, AnomaliasResponse, ConsejosResponse, AlertaPresupuestoResponse 
from src.ml.prediccion import predecir_gasto
from src.ml.anomalias import detectar_anomalia
from src.ml.consejos import generar_consejo
from src.ml.alertas_ml import verificar_presupuestos
from src.middleware.auth import verificar_token
from typing import List


router = APIRouter(prefix="/ml", tags=["ML"])

@router.get("/prediccion", response_model=PrediccionResponse)
def get_prediccion(db: Session = Depends(get_db), payload: dict = Depends(verificar_token)):
    usuario_id = payload.get("sub")
    try:
        prediccion = predecir_gasto(usuario_id, db)
        return prediccion
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/anomalias", response_model=AnomaliasResponse)
def get_anomalias(categoria_id: str, db: Session = Depends(get_db), payload: dict = Depends(verificar_token)):
    usuario_id = payload.get("sub")
    try:
        anomalia = detectar_anomalia(usuario_id, categoria_id, db)
        return anomalia
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.get("/consejos", response_model=ConsejosResponse)
def get_consejos(db: Session = Depends(get_db), payload: dict = Depends(verificar_token)):
    usuario_id = payload.get("sub")
    try:
        consejos = generar_consejo(usuario_id, db)
        return consejos
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.get("/alertas-presupuesto", response_model=List[AlertaPresupuestoResponse])
def get_alertas_presupuesto(db: Session = Depends(get_db), payload: dict = Depends(verificar_token)):
        usuario_id = payload.get("sub")
        try:
            alerta_presupuesto = verificar_presupuestos(usuario_id, db)
            return alerta_presupuesto
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    