from flask_sqlalchemy import SQLAlchemy
from geoalchemy2 import Geometry
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String, Float

# Conexión a PostgreSQL (modifica con tus credenciales)
DATABASE_URL = "postgresql://postgres:882311@localhost:5433/geojson"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Inicializa la base de datos con SQLAlchemy
db = SQLAlchemy()


# Define la tabla para almacenar datos geoespaciales
class PuntoInteres(Base):
    __tablename__ = "puntos_interes"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    descripcion = Column(String, nullable=True)
    capa = Column(String, nullable=True)
    latitud = Column(Float, nullable=False)
    longitud = Column(Float, nullable=False)
    geom = Column(Geometry("POINT"))  # Campo geoespacial


# Crear las tablas si no existen
Base.metadata.create_all(bind=engine)
