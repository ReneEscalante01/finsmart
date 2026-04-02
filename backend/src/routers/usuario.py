from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.database import get_db
from src.models.usuario import Usuario
from src.routers.auth import hashear_contrasena
from src.schemas.usuario import UsuarioResponse, UsuarioResponseModel, UsuarioUpdate
from src.middleware.rol import permiso_admin
from src.middleware.auth import verificar_token
from typing import List
from uuid import UUID

router = APIRouter(prefix="/usuarios", tags=["Usuario"])

@router.get("/", response_model=List[UsuarioResponse])
def get_usuarios(db: Session = Depends(get_db), payload: dict = Depends(permiso_admin)):
    try:
        usuarios = db.query(Usuario).all()
        return usuarios
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.get("/{id}", response_model=UsuarioResponse)
def get_usuarios(id: str, db: Session = Depends(get_db), payload: dict = Depends(verificar_token)):
    usuario_id = payload.get("sub")
    rol_id = payload.get("rol")
    try:
        id = UUID(id)
    except ValueError:
        raise HTTPException(status_code=400, detail="ID invalido")
        
    try:
        usuario = db.query(Usuario).filter(Usuario.id == id).first()
        if not usuario:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        if rol_id != 1 and str(usuario.id) != usuario_id:
            raise HTTPException(status_code=403, detail="No tienes permiso para ver este usuario")
        return usuario
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.patch("/{id}", response_model=UsuarioResponseModel)
def update_usuario(id: str, usuario: UsuarioUpdate, db: Session = Depends(get_db), payload: dict = Depends(verificar_token)):
    usuario_id = payload.get("sub")
    rol_id = payload.get("rol")
    try:
        id = UUID(id)
    except ValueError:
        raise HTTPException(status_code=400, detail="ID invalido")
    
    data = usuario.model_dump(exclude_unset=True)    
    if not data:
        raise HTTPException(status_code=400, detail="Debes enviar al menos un campo para actualizar")
    try:
        usuario = db.query(Usuario).filter(Usuario.id == id).first()
        if not usuario:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        if rol_id != 1 and str(usuario.id) != usuario_id:
            raise HTTPException(status_code=403, detail="No esta autorizado para editar el usuario")
        if "email" in data:
            exist = db.query(Usuario).filter(
                Usuario.email == data["email"],
                Usuario.id != id
            ).first()
            if exist:
                raise HTTPException(status_code=400, detail="Ya existe un usuario con ese correo electronico ")
        if "contrasena" in data:
            data["contrasena_hash"] = hashear_contrasena(data.pop("contrasena"))
        for key, value in data.items():
            setattr(usuario, key, value)
        db.commit()
        db.refresh(usuario)
        return UsuarioResponseModel(message="Usuario actualizado correctamente", data=usuario)
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    
@router.delete("/{id}", response_model=UsuarioResponseModel)
def delete_usuario(id: str, db: Session = Depends(get_db), payload: dict = Depends(verificar_token)):
    usuario_id = payload.get("sub")
    rol_id = payload.get("rol")
    
    try: 
        id = UUID(id)
    except ValueError:
        raise HTTPException(status_code=400, detail="ID invalido")
    
    try:
        usuario = db.query(Usuario).filter(Usuario.id == id).first()
        if not usuario:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        if rol_id != 1 and str(usuario.id) != usuario_id:
            raise HTTPException(status_code=403, detail="No esta autorizado para eliminar este campo")
        db.delete(usuario)
        db.commit()
        return UsuarioResponseModel(message="Usuario eliminado correctamente")
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))