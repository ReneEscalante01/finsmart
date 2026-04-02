from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from jose import jwt
from src.database import get_db
from src.models.usuario import Usuario
from src.schemas.usuario import UsuarioCreate, UsuarioResponseModel
from src.schemas.auth import UsuarioLogin, LoginResponse
from datetime import datetime, timedelta
import os

router = APIRouter(prefix="/auth", tags=["Auth"])
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

def hashear_contrasena(contrasena):
    return pwd_context.hash(contrasena)

def verificar_contrasena(contrasena, hash):
    return pwd_context.verify(contrasena, hash)

def crear_token(data: dict):
    datos = data.copy()
    expiracion = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    datos.update({"exp": expiracion})
    token = jwt.encode(datos, SECRET_KEY, algorithm=ALGORITHM)
    return token

@router.post("/registro", response_model= UsuarioResponseModel, status_code=201)
def registrar(usuario: UsuarioCreate, db: Session = Depends(get_db)):
    
    exist = db.query(Usuario).filter(Usuario.email == usuario.email).first()
    if exist:
        raise HTTPException(status_code=400, detail="Ya existe un usuario con ese correo electronico")
    
    try:
    
        nuevo_usuario = Usuario(
            nombre = usuario.nombre,
            email = usuario.email,
            contrasena_hash = hashear_contrasena(usuario.contrasena),
            moneda = usuario.moneda,
            rol_id = usuario.rol_id
        )
        db.add(nuevo_usuario)
        db.commit()
        db.refresh(nuevo_usuario)
        return UsuarioResponseModel(message = "Usuario registrado con exito", data = nuevo_usuario)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    
@router.post("/login", response_model=LoginResponse)
def login(usuario: UsuarioLogin, db: Session = Depends(get_db)):
    correo = db.query(Usuario).filter(Usuario.email == usuario.email).first()
    
    if not correo:
        raise HTTPException(status_code=400, detail= "Correo o contrasena incorrectos")
    
    if not verificar_contrasena(usuario.contrasena, correo.contrasena_hash):
        raise HTTPException(status_code=400, detail = "Correo o contrasena incorrectos")
    
    token = crear_token({"sub": str(correo.id), "rol": correo.rol_id})
    
    return{
        "message": "Login exitoso", 
        "access_token": token, 
        "token_type": "bearer"
        }
        