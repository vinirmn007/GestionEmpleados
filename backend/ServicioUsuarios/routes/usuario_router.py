from fastapi import APIRouter, Depends, HTTPException, status, Query, Header
from sqlalchemy.orm import Session
from typing import List
from database import SessionLocal
from schemas.usuario import UserRequest, UsuarioCreate, UsuarioRead, UserRolesResponse, UserIdResponse , PaginatedUsuarios, UsuarioUpdate
from models.usuario_model import Usuario
from crud.usuarioCrud import *
from utils.verify_roles import require_role, get_current_user


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


@router.post("/create", response_model=UsuarioRead, status_code=status.HTTP_201_CREATED)
def crear_usuario(usuario: UsuarioCreate, db: Session = Depends(get_db)):
    if get_user_by_email(db, usuario.correo):
        raise HTTPException(status_code=400, detail="El correo ya está registrado")
    if get_user_by_dni(db, usuario.dni):
        raise HTTPException(status_code=400, detail="El DNI ya está registrado")
    if get_user_by_celular(db, usuario.celular):
        raise HTTPException(status_code=400, detail="El celular ya está registrado")
    nuevo_usuario = create_user(db, usuario)
    return nuevo_usuario

@router.get("/all", response_model=list[UsuarioRead])

def listar_usuarios(db: Session = Depends(get_db), payload: dict = Depends(require_role("gerente"))):
    usuarios = db.query(Usuario).all()  
    return usuarios

@router.get("/list", response_model=PaginatedUsuarios)
def listar_usuarios_pag(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),

    db: Session = Depends(get_db),
    payload: dict = Depends(require_role("gerente"))
    ):
    total, usuarios = get_usuarios_paginated(db, skip, limit)
    return {
        "total": total,
        "skip": skip,
        "limit": limit,
        "data": usuarios
    }


@router.get("/get/{user_id}", response_model=UsuarioRead)
def obtener_usuario(user_id: int, db: Session = Depends(get_db)):
    usuario = get_user(db, user_id)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usuario

@router.get("/me", response_model=UsuarioRead)
def get_my_profile(current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    user_id = int(current_user["sub"])
    usuario = get_user(db, user_id)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usuario



@router.put("/update/{user_id}", response_model=UsuarioRead)
def actualizar_usuario(user_id: int, usuario: UsuarioUpdate, db: Session = Depends(get_db)):
    existente = get_user(db, user_id)
    if not existente:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    # Filtrar solo los campos que vienen en el request (excluir None)
    update_data = usuario.dict(exclude_unset=True)
    
    actualizado = update_user(db, user_id, **update_data)
    return actualizado



@router.delete("/delete/{user_id}", status_code=status.HTTP_204_NO_CONTENT)

def eliminar_usuario(user_id: int, db: Session = Depends(get_db), payload: dict = Depends(require_role("gerente"))):
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

@router.post("/roles", response_model=UserRolesResponse)
def user_roles(request: UserRequest, db: Session = Depends(get_db)):
    usuario = get_user_by_email(db, request.email)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return {"roles": [usuario.rol.value]}