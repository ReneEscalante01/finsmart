from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.database import get_db
from src.models.presupuesto import Presupuesto
from src.schemas.presupuesto import PresupuestoCreate, PresupuestoResponse, PresupuestoResponseModel, PresupuestoUpdate
from src.middleware.auth import verificar_token
from typing import List
from uuid import UUID

router = APIRouter(prefix="/presupuestos", tags=["Presupuestos"])

@router.post("/", response_model=PresupuestoResponseModel, status_code=201)
def create_presupuesto(presupuesto: PresupuestoCreate, db: Session = Depends(get_db), payload: dict = Depends(verificar_token)):
    usuario_id = payload.get("sub")
    
    exist = db.query(Presupuesto).filter(
        Presupuesto.usuario_id == usuario_id,
        Presupuesto.categoria_id == presupuesto.categoria_id,
        Presupuesto.periodo == presupuesto.periodo
        ).first()
    if exist:
        raise HTTPException(status_code=400, detail="Ya existe un presupuesto para esa categoria")

    try:
        nuevo_presupuesto = Presupuesto(
            monto_limite = presupuesto.monto_limite,
            periodo = presupuesto.periodo,
            fecha_inicio = presupuesto.fecha_inicio,
            fecha_fin = presupuesto.fecha_fin,
            usuario_id = usuario_id,
            categoria_id = presupuesto.categoria_id
        )
        db.add(nuevo_presupuesto)
        db.commit()
        db.refresh(nuevo_presupuesto)
        return PresupuestoResponseModel(message="Presupuesto creado correctamente", data=nuevo_presupuesto)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/", response_model=List[PresupuestoResponse])
def get_presupuestos(db: Session = Depends(get_db), payload: dict = Depends(verificar_token)):
    usuario_id = payload.get("sub")
    
    try:
        presupuesto = db.query(Presupuesto).filter(Presupuesto.usuario_id == usuario_id).all()
        return presupuesto
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{id}", response_model=PresupuestoResponse)
def get_presupuesto_by_id(id: str, db: Session = Depends(get_db), payload: dict = Depends(verificar_token)):
    usuario_id = payload.get("sub")
    
    try:
        id = UUID(id)
    except ValueError:
        raise HTTPException(status_code=400, detail="ID invalido")
    
    try:
        presupuesto = db.query(Presupuesto).filter(Presupuesto.id == id).first()
        if not presupuesto:
            raise HTTPException(status_code=404, detail="Presupuesto no encontrado")
        if str(presupuesto.usuario_id) != usuario_id:
            raise HTTPException(status_code=403, detail="No tienes permiso para ver este presupuesto")
        return presupuesto
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.patch("/{id}", response_model=PresupuestoResponseModel)
def update_presupuesto(id: str, presupuesto: PresupuestoUpdate, db: Session = Depends(get_db), payload: dict = Depends(verificar_token)):
    usuario_id = payload.get("sub")
    try:
        id = UUID(id)
    except ValueError:
        raise HTTPException(status_code=400, detail="ID invalido")
    
    data = presupuesto.model_dump(exclude_unset=True)
    if not data:
        raise HTTPException(status_code=400, detail="Debes enviar al menos un campo para actualizar")
    try:
        presupuesto = db.query(Presupuesto).filter(Presupuesto.id == id).first()
        if not presupuesto:
            raise HTTPException(status_code=404, detail="Presupuesto no encontrado")
        if str(presupuesto.usuario_id) != usuario_id:
            raise HTTPException(status_code=403, detail="No esta autorizado para editar este campo")
        
        for key, value in data.items():
            setattr(presupuesto, key, value)
        
        db.commit()
        db.refresh(presupuesto)
        return PresupuestoResponseModel(message= "Presupuesto actualizado correctamente", data=presupuesto)
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{id}", response_model=PresupuestoResponseModel)
def delete_presupuesto(id: str, db: Session = Depends(get_db), payload: dict = Depends(verificar_token)):
    usuario_id = payload.get("sub")
    
    try:
        id = UUID(id)
    except ValueError:
        raise HTTPException(status_code=400, detail="ID invalido")
    
    try:
        presupuesto = db.query(Presupuesto).filter(Presupuesto.id == id).first()
        if not presupuesto:
            raise HTTPException(status_code=404, detail="Presupuesto no encontrado")
        
        if str(presupuesto.usuario_id) != usuario_id:
            raise HTTPException(status_code=403, detail="No esta autorizado para eliminar este campo")
        
        db.delete(presupuesto)
        db.commit()
        return PresupuestoResponseModel(message = "Presupuesto eliminado correctamente")
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    
