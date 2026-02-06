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


def require_role(role: str, auto_error: bool = True):
    async def role_dependency(payload: dict = Depends(get_current_user)):
        user_roles = payload.get("roles", [])
        
        # Normalize to list if string
        if isinstance(user_roles, str):
            user_roles = [user_roles]

        print(f"DEBUG ROLE CHECK: User Roles: {user_roles}, Required: {role}")

        # Hierarchy: Gerente has all permissions of Empleado
        if role == "empleado" and "gerente" in user_roles:
            return payload

        if role not in user_roles:
            print(f"DEBUG: Role '{role}' NOT found in {user_roles}")
            if auto_error:
                raise HTTPException(
                    status_code=403, detail=f"Se requiere rol '{role}' para acceder a este recurso. Roles actuales: {user_roles}"
                )
            else:
                return None
        return payload
    return role_dependency