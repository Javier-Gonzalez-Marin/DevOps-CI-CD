import enum
from sqlalchemy import Column, Integer, String, Float, ForeignKey, Enum
from sqlalchemy.orm import relationship
from .database import Base

class EstadoPatinete(str, enum.Enum):
    disponible = "disponible"
    en_uso = "en_uso"
    mantenimiento = "mantenimiento"
    sin_bateria = "sin_bateria"

class Zone(Base):
    __tablename__ = "zones"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String)
    codigo_postal = Column(String)
    limite_velocidad = Column(Integer)
    scooters = relationship("Scooter", back_populates="zona")

class Scooter(Base):
    __tablename__ = "scooters"
    id = Column(Integer, primary_key=True, index=True)
    numero_serie = Column(String, unique=True)
    modelo = Column(String)
    bateria = Column(Integer)
    estado = Column(Enum(EstadoPatinete), default=EstadoPatinete.disponible)
    zona_id = Column(Integer, ForeignKey("zones.id"))
    puntuacion_usuario = Column(Float, nullable=True)
    zona = relationship("Zone", back_populates="scooters")