
import sys
import os
import jwt
from datetime import datetime, timedelta, timezone

# Add current directory to path to allow imports
sys.path.append(os.getcwd())

# Mock settings
class MockSettings:
    AUTHJWT_SECRET_KEY = "alexisjosue12345"

# Mock verify_roles logic imports
# We can't easily import verify_roles because it depends on secret_keys_settings which depends on .env
# We will just replicate the logic to see if it fails with the same library version.

SECRET_KEY = "alexisjosue12345"
ALGORITHM = "HS256"

def create_valid_token():
    expire = datetime.now(timezone.utc) + timedelta(hours=1)
    to_encode = {
        "sub": 1,
        "roles": "gerente",
        "exp": expire
    }
    # Emulate ServicioAutenticacion (PyJWT 1.7.1 default behavior logic, but we are running in ServicioUsuarios env with PyJWT 2.10.1)
    # PyJWT 2.10.1 encode returns str. PyJWT 1.7.1 returns bytes.
    # The secret and algo are the same.
    token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    print(f"Generated Token: {token}")
    return token

def verify_token(token):
    try:
        if isinstance(token, bytes):
            token = token.decode('utf-8')
            
        print(f"Attempting to decode with key: {SECRET_KEY} and algo: {ALGORITHM}")
        # Emulate ServicioUsuarios (PyJWT 2.10.1)
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        print("Success! Payload:", payload)
    except jwt.ExpiredSignatureError:
        print("Error: Token Expired")
    except jwt.InvalidTokenError as e:
        print(f"Error: Invalid Token - {e}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    print(" reproducing 401...")
    token = create_valid_token()
    verify_token(token)
