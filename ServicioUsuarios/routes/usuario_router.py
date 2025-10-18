from fastapi import APIRouter, HTTPException
from typing import List
from models.usuario_model import Usuario, UsuarioCreate, PasswordCreate


router = APIRouter(
    prefix="/users",
    tags=["Usuarios"]
)

# Simulación temporal de "base de datos"
usuarios_db = [
    Usuario(id=1, nombres="Ana", apellidos="López", email="ana@empresa.com", celular="0999999999", rol="empleado"),
    Usuario(id=2, nombres="Carlos", apellidos="Pérez", email="carlos@empresa.com", celular="0988888888", rol="supervisor"),
]

# -----------------------------------------------------
#  POST /users/register → crear nuevo empleado
# -----------------------------------------------------
@router.post("/register", response_model=Usuario, status_code=201)
def registrar_usuario(usuario: UsuarioCreate):
    nuevo_id = len(usuarios_db) + 1
    nuevo_usuario = Usuario(id=nuevo_id, **usuario.dict())
    usuarios_db.append(nuevo_usuario)
    return nuevo_usuario

# -----------------------------------------------------
#  GET /users → listar empleados
# -----------------------------------------------------
@router.get("/", response_model=List[Usuario])
def listar_usuarios():
    return usuarios_db

# Usuario simulado como "autenticado"
usuario_actual = Usuario(
    id=1,
    nombres="Ana",
    apellidos="López",
    email="ana@empresa.com",
    celular="0999999999",
    rol="empleado"
)

@router.get("/me", response_model=Usuario)
def obtener_mi_perfil():
    return usuario_actual

# -----------------------------------------------------
# GET /users/{user_id} → obtener detalles de un empleado
# -----------------------------------------------------
@router.get("/{user_id}", response_model=Usuario)
def obtener_usuario(user_id: int):
    for usuario in usuarios_db:
        if usuario.id == user_id:
            return usuario
    raise HTTPException(status_code=404, detail="Usuario no encontrado")

# -----------------------------------------------------
# PUT /users/{user_id} → actualizar información del usuario
# -----------------------------------------------------
@router.put("/{user_id}", response_model=Usuario)
def actualizar_usuario(user_id: int, datos: UsuarioCreate):
    for i, usuario in enumerate(usuarios_db):
        if usuario.id == user_id:
            actualizado = Usuario(id=user_id, **datos.dict())
            usuarios_db[i] = actualizado
            return actualizado
    raise HTTPException(status_code=404, detail="Usuario no encontrado")



@router.post("/set-password")
def set_password(datos: PasswordCreate):
    for usuario in usuarios_db:
        if usuario.id == datos.user_id:
            usuario.password = datos.password  # Guardar la contraseña
            return {"message": "Contraseña establecida correctamente"}
    raise HTTPException(status_code=404, detail="Usuario no encontrado")




