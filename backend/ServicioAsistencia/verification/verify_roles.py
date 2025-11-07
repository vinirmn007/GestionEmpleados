from fastapi import Depends, HTTPException, Header
import jwt

from .settings import settings

SECRET_KEY = settings.AUTHJWT_SECRET_KEY
ALGORITHM = "HS256"


def decode_jwt(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expirado")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Token inválido")


async def get_current_user(authorization: str = Header(...)):
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Encabezado Authorization inválido")

    token = authorization.split(" ")[1]
    payload = decode_jwt(token)
    return payload


def require_role(role: str):
    async def role_dependency(payload: dict = Depends(get_current_user)):
        user_roles = payload.get("roles", [])
        if role not in user_roles:
            raise HTTPException(
                status_code=403, detail=f"Se requiere rol '{role}' para acceder a este recurso"
            )
        return payload
    return role_dependency