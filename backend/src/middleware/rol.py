from fastapi import HTTPException, Depends
from src.middleware.auth import verificar_token

def permiso_admin(payload: dict = Depends(verificar_token)):
    if payload.get("rol") != 1:
        raise HTTPException(status_code=403, detail="No tienes permisos para realizar esta accion")
    return payload