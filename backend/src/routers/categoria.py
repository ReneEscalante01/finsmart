from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.database import get_db
from src.models.categoria import Categoria
from src.schemas.categoria import CategoriaCreate, CategoriaResponse, CategoriaUpdate, CategoriaResponseModel
from src.middleware.auth import verificar_token
from typing import List
from uuid import UUID
from sqlalchemy import or_

router = APIRouter(prefix="/categorias", tags=["Categorias"])

@router.post("/", response_model = CategoriaResponseModel, status_code = 201)
def create_categoria(categoria: CategoriaCreate,  db: Session = Depends(get_db), payload: dict = Depends(verificar_token)):
    usuario_id = payload.get("sub")
    
    exist = db.query(Categoria).filter(Categoria.nombre == categoria.nombre).first()
    if exist:
        raise HTTPException(status_code = 400, detail = "Ya existe una categoria con ese nombre")
    
    try:
        nueva_categoria = Categoria(
            nombre = categoria.nombre,
            icono = categoria.icono,
            color = categoria.color,
            es_default = categoria.es_default,
            usuario_id = usuario_id 
        )
        db.add(nueva_categoria)
        db.commit()
        db.refresh(nueva_categoria)
        return CategoriaResponseModel(message="Categoria creada correctamente", data=nueva_categoria)
    
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code = 500, detail=str(e))
    
@router.get("/", response_model = List[CategoriaResponse])
def get_categoria(db: Session = Depends(get_db), payload: dict = Depends(verificar_token)):
    usuario_id = payload.get("sub")
    try:
        categorias = db.query(Categoria).filter(
            or_(Categoria.es_default == True, Categoria.usuario_id == usuario_id)
        ).all()
        return categorias
    except Exception as e:
        raise HTTPException(status_code = 500, detail=str(e))
    
@router.get("/{id}", response_model = CategoriaResponse)
def get_categoria_by_Id(id: str, db: Session = Depends(get_db), payload: dict = Depends(verificar_token)):
    usuario_id = payload.get("sub")
    try:
        id =UUID(id) 
    except ValueError:
        raise HTTPException(status_code=400, detail = "ID invalido")
    
    try:
        categoria = db.query(Categoria).filter(Categoria.id == id).first()
        if not categoria:
            raise HTTPException(status_code=404, detail="Categoria no encontrada")
        if not categoria.es_default and str(categoria.usuario_id) != usuario_id:
            raise HTTPException(status_code=403, detail="No tienes permiso para ver esta categoria")
        return categoria
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.patch("/{id}", response_model=CategoriaResponseModel)
def update_categoria(id: str, categoria: CategoriaUpdate, db: Session = Depends(get_db), payload: dict = Depends(verificar_token)):
    usuario_id = payload.get("sub")
    try:
        id = UUID(id)
    except ValueError:
        raise HTTPException(status_code=400, detail="ID invalido")
    
    data = categoria.model_dump(exclude_unset=True)
    if not data:
        raise HTTPException(status_code=400, detail= "Debes enviar al menos un campo para actualizar")
    
    try:
        categoria = db.query(Categoria).filter(Categoria.id ==id).first()
        if not categoria:
            raise HTTPException(status_code=404, detail="Categoria no encontrada")
        if categoria.es_default == True:
            raise HTTPException(status_code=403, detail = "No esta autorizado para editar este campo")
        if str(categoria.usuario_id) != usuario_id:
            raise HTTPException(status_code=403, detail = "No esta autorizado para editar este campo")
        if "nombre" in data:
            exist = db.query(Categoria).filter(
                Categoria.nombre == data["nombre"],
                Categoria.id != id
            ).first()
            if exist:
                raise HTTPException(status_code=400, detail="Ya existe una categoria con ese nombre")
        
        for key, value in data.items():
            setattr(categoria, key, value)
        
        db.commit()
        db.refresh(categoria)
        return CategoriaResponseModel(message="Categoria actualizada correctamente", data=categoria)
    
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    
@router.delete("/{id}", response_model= CategoriaResponseModel, status_code=200)
def delete_categoria(id: str, db: Session = Depends(get_db), payload: dict = Depends(verificar_token)):
    usuario_id = payload.get("sub")
    try:
        id = UUID(id)
    except ValueError:
        raise HTTPException(status_code=400, detail="ID invalido")
    
    try:
        categoria = db.query(Categoria).filter(Categoria.id == id).first()
        if not categoria:
            raise HTTPException(status_code=404, detail="Categoria no encontrada")
        if categoria.es_default == True:
            raise HTTPException(status_code=403, detail="No esta autorizado para eliminar este campo")
        if str(categoria.usuario_id) != usuario_id:
            raise HTTPException(status_code=403, detail="No esta autorizado para eliminar este campo")
        db.delete(categoria)
        db.commit()
        return CategoriaResponseModel(message="Categoria eliminada correctamente")
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
