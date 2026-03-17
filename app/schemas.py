from pydantic import BaseModel, Field
from typing import Optional
from .models import EstadoPatinete

class ScooterBase(BaseModel):
    numero_serie: str
    modelo: str
    bateria: int = Field(ge=0, le=100)
    estado: EstadoPatinete
    zona_id: int

class ScooterCreate(ScooterBase):
    pass

class ScooterResponse(ScooterBase):
    id: int
    puntuacion_usuario: Optional[float] = None
    class Config:
        from_attributes = True

class ZoneCreate(BaseModel):
    nombre: str
    codigo_postal: str
    limite_velocidad: int