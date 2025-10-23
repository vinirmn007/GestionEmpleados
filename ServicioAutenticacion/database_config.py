from sqlalchemy import create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from secret_keys_settings import settings

#configuracion de la base de datos
DB_HOST = settings.DB_HOST
DB_USER = settings.DB_USER
DB_PASSWORD = settings.DB_PASSWORD
DB_NAME = "db_auth"

#url de la base de datos sin especificar 
DB_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:3306"

#url de la db para este servicio
SPECIFYC_DB_URL = f"{DB_URL}/{DB_NAME}"

#crea la base si no existe
try:
    temp_engine = create_engine(DB_URL)
    with temp_engine.connect() as conn:
        conn.execute(text(f"CREATE DATABASE IF NOT EXISTS {DB_NAME}"))
        conn.commit()
except Exception as e:
    print(f"Error al crear la base de datos {DB_NAME}: {e}")
    pass

#configuracion del SQLAlchemy
engine = create_engine(SPECIFYC_DB_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()