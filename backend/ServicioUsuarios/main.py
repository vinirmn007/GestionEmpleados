from fastapi import FastAPI
from database import Base, engine
from routes.usuario_router import router as usuario_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Servicio Usuarios")

#origenes permitidos
origins = [
    #Para pruebas:"http://localhost:9000"
    #"http://servicio-autenticacion:9000" #ruta del docker-compose
    "*"
]

#cinfigurar cors
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["get"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"mensaje": "¡Hola, Servicio Usuarios está funcionando!"}

app.include_router(usuario_router)
Base.metadata.create_all(bind=engine)