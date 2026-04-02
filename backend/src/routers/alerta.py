from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.database import get_db
from src.models.alerta import Alerta
from src.schemas.alerta import  AlertaResponse, AlertaResponseModel, AlertaUpdate
from src.middleware.auth import verificar_token
from typing import List
from uuid import UUID

router = APIRouter(prefix="/alertas", tags=["Alertas"])

@router.get("/", response_model=List[AlertaResponse])
def get_alertas(db: Session = Depends(get_db), payload: dict = Depends(verificar_token)):
    usuario_id = payload.get("sub")
    
    try:
        alertas = db.query(Alerta).filter(Alerta.usuario_id == usuario_id).all()
        return alertas
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.get("/{id}", response_model=AlertaResponse)
def get_alerta_by_id(id: str, db: Session = Depends(get_db), payload: dict = Depends(verificar_token)):
    usuario_id = payload.get("sub")
    
    try:
        id = UUID(id)
    except ValueError:
        raise HTTPException(status_code=400, detail="ID invalido")
    
    try:
        alerta = db.query(Alerta).filter(Alerta.id == id).first()
        if not alerta:
            raise HTTPException(status_code=404, detail="Alerta no encontrada")
        if str(alerta.usuario_id) != usuario_id:
            raise HTTPException(status_code=403, detail="No tienes permiso para ver esta alerta")
        return alerta
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.patch("/{id}", response_model= AlertaResponseModel)
def marcar_alerta(id: str, alerta: AlertaUpdate, db: Session = Depends(get_db), payload: dict = Depends(verificar_token)):
    usuario_id = payload.get("sub")
    
    try:
        id = UUID(id)
    except ValueError:
        raise HTTPException(status_code=400, detail="ID invalido")
    
    data = alerta.model_dump(exclude_unset=True)
    
    try:
        alerta = db.query(Alerta).filter(Alerta.id == id).first()
        if not alerta:
            raise HTTPException(status_code=404, detail="Alerta no encontrada")
        if str(alerta.usuario_id) != usuario_id:
            raise HTTPException(status_code=403, detail="No tienes permiso para modificar este campo")
        
        for key, value, in data.items():
            setattr(alerta, key, value)
        
        db.commit()
        db.refresh(alerta)
        if alerta.leida == False:
            return AlertaResponseModel(message="Alerta marcada como leida")
        return AlertaResponseModel(message="Alerta marcada como no leida")
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    