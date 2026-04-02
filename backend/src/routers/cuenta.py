from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.database import get_db
from src.models.cuenta import Cuenta
from src.schemas.cuenta import CuentaCreate, CuentaResponse, CuentaUpdate, CuentaResponseModel
from src.middleware.auth import verificar_token
from typing import List
from uuid import UUID

router = APIRouter(prefix="/cuentas", tags=["Cuentas"])

@router.post("/", response_model=CuentaResponseModel, status_code=201)
def create_cuenta(cuenta: CuentaCreate, db: Session = Depends(get_db), payload: dict = Depends(verificar_token)):
    usuario_id = payload.get("sub")
    
    exist = db.query(Cuenta).filter(
        Cuenta.nombre == cuenta.nombre,
        Cuenta.usuario_id == usuario_id
        ).first()
    if exist:
        raise HTTPException(status_code=400, detail = "Ya existe una cuenta con ese nombre")
    
    try:
        nueva_cuenta = Cuenta(
            nombre = cuenta.nombre,
            tipo = cuenta.tipo,
            saldo_inicial = cuenta.saldo_inicial,
            saldo_actual = cuenta.saldo_actual,
            usuario_id = usuario_id
        )
        db.add(nueva_cuenta)
        db.commit()
        db.refresh(nueva_cuenta)
        return CuentaResponseModel(message = "Cuenta creada correctamente", data = nueva_cuenta)
    
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail = str(e))

@router.get("/", response_model= List[CuentaResponse])
def get_cuentas(db: Session = Depends(get_db), payload: dict = Depends(verificar_token)):
    usuario_id = payload.get("sub")
    
    try:
        cuentas = db.query(Cuenta).filter(Cuenta.usuario_id == usuario_id).all()
        return cuentas
    except Exception as e:
        raise HTTPException(status_code=500, detail = str(e))
    
@router.get("/{id}", response_model=CuentaResponse)
def get_cuenta_by_id(id: str, db: Session = Depends(get_db), payload: dict = Depends(verificar_token)):
    usuario_id = payload.get("sub")
    try:
        id = UUID(id)
    except ValueError:
        raise HTTPException(status_code=400, detail = "ID invalido")
    
    try:
        cuenta = db.query(Cuenta).filter(Cuenta.id == id).first()
        if not cuenta:
            raise HTTPException(status_code=404, detail="Cuenta no encontrada")
        if str(cuenta.usuario_id) != usuario_id:
            raise HTTPException(status_code=403, detail = "No tienes permiso para ver esa cuenta")
        return cuenta
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail = str(e))
    
@router.patch("/{id}", response_model=CuentaResponseModel)
def update_cuenta(id: str, cuenta: CuentaUpdate, db: Session = Depends(get_db), payload: dict = Depends(verificar_token)):
    usuario_id = payload.get("sub")
    
    try:
        id = UUID(id)
    except ValueError:
        raise HTTPException(status_code=400, detail="ID invalido")
    
    data = cuenta.model_dump(exclude_unset=True)
    if not data:
        raise HTTPException(status_code=400, detail = "Debes enviar al menos un campo para actualizar")
    
    try:
        cuenta = db.query(Cuenta).filter(Cuenta.id == id).first()
        if not cuenta:
            raise HTTPException(status_code=404, detail="Cuenta no encontrada")
        if str(cuenta.usuario_id) != usuario_id:
            raise HTTPException(status_code=403, detail="No esta autorizado para editar este campo")
        if "nombre" in data:
            exist = db.query(Cuenta).filter(
                Cuenta.nombre == data["nombre"],
                Cuenta.id != id
            ).first()
            if exist:
                raise HTTPException(status_code=400, detail="Ya existe una cuenta con ese nombre")
            
        for key, value in data.items():
            setattr(cuenta, key, value)
        
        db.commit()
        db.refresh(cuenta)
        return CuentaResponseModel(message="Cuenta actualizada correctamente", data=cuenta)
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{id}", response_model=CuentaResponseModel, status_code=200)
def delete_cuenta(id: str, db: Session = Depends(get_db), payload: dict = Depends(verificar_token)):

    usuario_id = payload.get("sub")
    
    try:
        id = UUID(id)
    except ValueError:
        raise HTTPException(status_code=400, detail="ID invalido")
    
    try:
        cuenta = db.query(Cuenta).filter(Cuenta.id == id).first()
        if not cuenta:
            raise HTTPException(status_code=404, detail="Cuenta no encontrada")
        if str(cuenta.usuario_id) != usuario_id:
            raise HTTPException(status_code=403, detail="No esta autorizado para eliminar este campo")
        db.delete(cuenta)
        db.commit()
        return CuentaResponseModel(message="Cuenta eliminada correctamente")
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    