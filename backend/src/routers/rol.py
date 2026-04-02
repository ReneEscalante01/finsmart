from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.database import get_db
from src.models.rol import Rol
from src.schemas.rol import RolCreate, RolResponse, RolResponseModel, RolUpdate
from src.middleware.rol import permiso_admin
from src.middleware.auth import verificar_token
from typing import List
from uuid import UUID

router = APIRouter(prefix="/roles", tags=["Roles"])

@router.post("/", response_model=RolResponseModel)
def create_rol(rol: RolCreate, db: Session = Depends(get_db), payload: dict = Depends(permiso_admin)):
    exist = db.query(Rol).filter(Rol.nombre_rol == rol.nombre_rol).first()
    if exist:
        raise HTTPException(status_code=400, detail="Ya existe un rol con ese nombre")
    try:
        nuevo_rol = Rol(
            nombre_rol = rol.nombre_rol
        )
        db.add(nuevo_rol)
        db.commit()
        db.refresh(nuevo_rol)
        return RolResponseModel(message="Rol creado correctamente", data=nuevo_rol)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/", response_model=List[RolResponse])
def get(db: Session = Depends(get_db), payload: dict = Depends(permiso_admin)):
    try:
        roles = db.query(Rol).all()
        return roles
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{id}", response_model=RolResponse)
def get_rol_by_id(id: int, db: Session = Depends(get_db), payload: dict = Depends(permiso_admin)):
    try:
        rol = db.query(Rol).filter(Rol.id == id).first()
        if not rol:
            raise HTTPException(status_code=404, detail="Rol no encontrado")
        return rol
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.patch("/{id}", response_model=RolResponseModel)
def update_rol(id: int, rol: RolUpdate, db: Session = Depends(get_db), payload: dict = Depends(permiso_admin)):
    data = rol.model_dump(exclude_unset=True)
    if not data:
        raise HTTPException(status_code=400, detail="Debes enviar al menos un campo para actualizar")
    try:
        rol = db.query(Rol).filter(Rol.id == id).first()
        if not rol:
            raise HTTPException(status_code=404, detail="Rol no encontrado")
        if "nombre_rol" in data:
            exist = db.query(Rol).filter(
                Rol.nombre_rol == data["nombre_rol"],
                Rol.id != id
            ).first()
            if exist:
                raise HTTPException(status_code=400, detail="Ya existe un rol con ese nombre")
        for key, value in data.items():
            setattr(rol, key, value)
            
        db.commit()
        db.refresh(rol)
        return RolResponseModel(message="Rol actualizado correctamente", data=rol)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.delete("/{id}", response_model=RolResponseModel)
def delete_rol(id: int, db: Session = Depends(get_db), payload: dict = Depends(permiso_admin)):
    try:
        rol = db.query(Rol).filter(Rol.id == id).first()
        if not rol:
            raise HTTPException(status_code=404, detail="Rol no encontrado")
        db.delete(rol)
        db.commit()
        return RolResponseModel(message="Rol eliminado correctamente")
    except HTTPException:
        raise 
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))