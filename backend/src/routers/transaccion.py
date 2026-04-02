from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.database import get_db
from src.models.transaccion import Transaccion
from src.schemas.transaccion import TransaccionCreate, TransaccionResponse, TransaccionResponseModel
from src.models.cuenta import Cuenta
from src.middleware.auth import verificar_token
from typing import List
from uuid import UUID

router = APIRouter(prefix="/transacciones", tags=["Transacciones"])

@router.post("/", response_model=TransaccionResponseModel, status_code=201)
def create_transaccion(transaccion: TransaccionCreate, db: Session = Depends(get_db), payload: dict = Depends(verificar_token)):
    usuario_id = payload.get("sub")
    try:
        cuenta = db.query(Cuenta).filter(Cuenta.id == transaccion.cuenta_id).first()
        if not cuenta: 
            raise HTTPException(status_code=404, detail="Cuenta no encontrada")
        if str(cuenta.usuario_id) != usuario_id:
            raise HTTPException(status_code=400, detail="No tienes permiso para usar esta cuenta")
        nueva_transaccion = Transaccion(
            monto = transaccion.monto,
            tipo = transaccion.tipo,
            nota = transaccion.nota,
            fecha = transaccion.fecha,
            usuario_id = usuario_id,
            cuenta_id = transaccion.cuenta_id,
            categoria_id = transaccion.categoria_id
        )
        if transaccion.tipo == "ingreso":
            cuenta.saldo_actual += transaccion.monto
        elif transaccion.tipo == "gasto":
            cuenta.saldo_actual -= transaccion.monto
            
        db.add(nueva_transaccion)
        db.commit()
        db.refresh(nueva_transaccion)
        return TransaccionResponseModel(message="Transaccion creada correctamente", data=nueva_transaccion)
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    
@router.get("/", response_model=List[TransaccionResponse])
def get_transacciones(db: Session = Depends(get_db), payload: dict = Depends(verificar_token)):
    usuario_id = payload.get("sub")
    try:
        transacciones = db.query(Transaccion).filter(
            Transaccion.usuario_id == usuario_id
        ).all()
        return transacciones
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{id}", response_model=TransaccionResponse)
def get_transaccion_by_id(id: str, db: Session = Depends(get_db), payload: dict = Depends(verificar_token)):
    usuario_id = payload.get("sub")
    
    try:
        id = UUID(id)
    except ValueError:
        raise HTTPException(status_code=400, detail="ID invalido")
    
    try:
        transaccion = db.query(Transaccion).filter(Transaccion.id == id).first()
        if not transaccion:
            raise HTTPException(status_code=404, detail="Transaccion no encontrada")
        if str(transaccion.usuario_id) != usuario_id:
            raise HTTPException(status_code=403, detail="No tienes permiso para ver esta transaccion")
        return transaccion
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
            
@router.delete("/{id}", response_model=TransaccionResponseModel)
def delete_transaccion(id: str, db: Session = Depends(get_db), payload: dict = Depends(verificar_token)):
    usuario_id = payload.get("sub")
    
    try:
        id = UUID(id)
    except ValueError:
        raise HTTPException(status_code=400, detail="ID invalido")
    
    try:
        transaccion = db.query(Transaccion).filter(Transaccion.id == id).first()
        if not transaccion:
            raise HTTPException(status_code=404, detail="Transaccion no encontrada")
        if str(transaccion.usuario_id) != usuario_id:
            raise HTTPException(status_code=403, detail="No esta autorizado para eliminar este campo")
        cuenta = db.query(Cuenta).filter(Cuenta.id == transaccion.cuenta_id).first()
        if transaccion.tipo == "ingreso":
            cuenta.saldo_actual -= transaccion.monto
        elif transaccion.tipo == "gasto":
            cuenta.saldo_actual += transaccion.monto
        db.delete(transaccion)
        db.commit()
        return TransaccionResponseModel(message="Transaccion eliminada correctamente")
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))