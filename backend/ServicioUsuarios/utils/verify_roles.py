from fastapi import Depends, HTTPException, Header
import jwt
from datetime import datetime
from secret_keys_settings import settings

SECRET_KEY = settings.AUTHJWT_SECRET_KEY
ALGORITHM = "HS256"


def decode_jwt(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        print(f"DEBUG: Token expired. Server time: {datetime.now()}")
        raise HTTPException(status_code=401, detail="Token expirado")
    except jwt.InvalidTokenError as e:
        print(f"DEBUG: Invalid Token. Error: {e}")
        print(f"DEBUG: Token received: {token}")
        print(f"DEBUG: Secret Key used: {SECRET_KEY}")
        raise HTTPException(status_code=401, detail=f"Token inválido: {e}")


async def get_current_user(authorization: str = Header(None)):
    if not authorization:
        raise HTTPException(status_code=401, detail="No se proporcionó token de autenticación")

    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Encabezado Authorization inválido")

    token = authorization.split(" ")[1]
    payload = decode_jwt(token)
    return payload


def require_role(role: str):
    async def role_dependency(payload: dict = Depends(get_current_user)):
        user_roles = payload.get("roles")
        
        if user_roles is None:
             raise HTTPException(
                status_code=403, detail="El token no contiene roles"
            )

        # Si user_roles es un string (como en este caso "gerente"), lo comparamos directamente
        if isinstance(user_roles, str):
            if user_roles != role:
                 raise HTTPException(
                    status_code=403, detail=f"Se requiere rol '{role}' para acceder a este recurso"
                )
        # Si fuera una lista, verificamos pertenencia (futura compatibilidad)
        elif isinstance(user_roles, list):
            if role not in user_roles:
                 raise HTTPException(
                    status_code=403, detail=f"Se requiere rol '{role}' para acceder a este recurso"
                )
        else:
             raise HTTPException(
                status_code=403, detail="Formato de roles inválido en el token"
            )
            
        return payload
    return role_dependency
