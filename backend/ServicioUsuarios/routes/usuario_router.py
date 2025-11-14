from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List
from database import SessionLocal
from schemas.usuario import UserRequest, UsuarioCreate, UsuarioRead, UserRolesResponse, UserIdResponse , PaginatedUsuarios
from models.usuario_model import Usuario
from crud.usuarioCrud import (
    get_user,
    get_user_by_email,
    create_user,
    update_user,
    delete_user,
    verify_user_password,
    get_usuarios_paginated
)

router = APIRouter(
    prefix="/usuarios",
    tags=["Usuarios"]
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=UsuarioRead, status_code=status.HTTP_201_CREATED)
def crear_usuario(usuario: UsuarioCreate, db: Session = Depends(get_db)):
    existente = get_user_by_email(db, usuario.correo)
    if existente:
        raise HTTPException(status_code=400, detail="Correo ya registrado")
    nuevo_usuario = create_user(db, usuario)
    return nuevo_usuario

@router.get("/", response_model=list[UsuarioRead])
def listar_usuarios(db: Session = Depends(get_db)):
    usuarios = db.query(Usuario).all()  
    return usuarios

@router.get("/list", response_model=PaginatedUsuarios)
def listar_usuarios(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db)
    ):
    total, usuarios = get_usuarios_paginated(db, skip, limit)
    return {
        "total": total,
        "skip": skip,
        "limit": limit,
        "data": usuarios
    }


@router.get("/{user_id}", response_model=UsuarioRead)
def obtener_usuario(user_id: int, db: Session = Depends(get_db)):
    usuario = get_user(db, user_id)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usuario



@router.put("/{user_id}", response_model=UsuarioRead)
def actualizar_usuario(user_id: int, usuario: UsuarioCreate, db: Session = Depends(get_db)):
    existente = get_user(db, user_id)
    if not existente:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    actualizado = update_user(
        db, user_id,
        nombre=usuario.nombre,
        correo=usuario.correo
    )
    return actualizado



@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_usuario(user_id: int, db: Session = Depends(get_db)):
    eliminado = delete_user(db, user_id)
    if not eliminado:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return None

@router.post("/validate", response_model=UsuarioRead)
def validate_user(request: UserRequest, db: Session = Depends(get_db)):
    usuario = get_user_by_email(db, request.email)

    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    is_valid = verify_user_password(db, request.email, request.password)
    if not is_valid:
        raise HTTPException(status_code=401, detail="Credenciales inválidas")
    
    return usuario


@router.post("/user_id", response_model=UserIdResponse)
def user_id(request: UserRequest, db: Session = Depends(get_db)):
    usuario = get_user_by_email(db, request.email)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return {"user_id": usuario.id}


@router.post("/roles", response_model=UserRolesResponse)
def user_roles(request: UserRequest, db: Session = Depends(get_db)):
    usuario = get_user_by_email(db, request.email)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return {"roles": [usuario.rol.value]}