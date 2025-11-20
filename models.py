from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from enum import Enum
from datetime import datetime
from pydantic import BaseModel, validator
from datetime import timedelta 
import re

# Zona horaria Argentina
def hora_argentina():
    return datetime.utcnow() - timedelta(hours=3)

# Modelos Base
class AutoBase(SQLModel):
    marca: str = Field(index=True)
    modelo: str = Field(index=True)
    anio: int = Field(gt=1900, lt=2030)
    numero_chasis: str = Field(index=True, unique=True)
    precio: float = Field(gt=0)
    kilometraje: float = Field(ge=0)
    color: str
    tipo_combustible: str
    descripcion: Optional[str] = None
    imagen_url: Optional[str] = None

class VentaBase(SQLModel):
    nombre_comprador: str
    precio: float = Field(gt=0)
    fecha_venta: datetime = Field(default_factory=hora_argentina)

# Modelos de Tabla con Relaciones
class Auto(AutoBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    estado: str = Field(default="disponible")
    fecha_ingreso: datetime = Field(default_factory=hora_argentina)
    
    # Relación uno-a-muchos con Ventas
    ventas: List["Venta"] = Relationship(back_populates="auto")

class Venta(VentaBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    auto_id: int = Field(foreign_key="auto.id")
    
    # Relación muchos-a-uno con Auto
    auto: Auto = Relationship(back_populates="ventas")

# Modelos para Creación
class AutoCreate(AutoBase):
    @validator('numero_chasis')
    def validar_chasis(cls, v):
        if not re.match(r'^[A-Z0-9]{10,20}$', v):
            raise ValueError('Número de chasis debe ser alfanumérico (10-20 caracteres)')
        return v

class VentaCreate(BaseModel):
    nombre_comprador: str
    precio: float = Field(gt=0)
    auto_id: int
    fecha_venta: datetime = Field(default_factory=hora_argentina)
    
    @validator('nombre_comprador')
    def nombre_no_vacio(cls, v):
        if not v or not v.strip():
            raise ValueError('Nombre del comprador no puede estar vacío')
        return v.strip()
    
    @validator('fecha_venta')
    def fecha_no_futura(cls, v):
        if v > hora_argentina():
            raise ValueError('La fecha de venta no puede ser futura')
        return v

# Modelos para Actualización
class AutoUpdate(BaseModel):
    marca: Optional[str] = None
    modelo: Optional[str] = None
    anio: Optional[int] = None
    precio: Optional[float] = None
    kilometraje: Optional[float] = None
    color: Optional[str] = None
    tipo_combustible: Optional[str] = None
    descripcion: Optional[str] = None
    imagen_url: Optional[str] = None
    estado: Optional[str] = None

class VentaUpdate(BaseModel):
    nombre_comprador: Optional[str] = None
    precio: Optional[float] = None
    
    @validator('nombre_comprador')
    def nombre_no_vacio(cls, v):
        if v is not None and (not v or not v.strip()):
            raise ValueError('Nombre del comprador no puede estar vacío')
        return v.strip() if v else v

# Modelos para Respuesta
class AutoResponse(AutoBase):
    id: int
    estado: str
    fecha_ingreso: datetime

class VentaResponse(VentaBase):
    id: int
    auto_id: int

class AutoResponseWithVentas(AutoResponse):
    ventas: List[VentaResponse] = []

class VentaResponseWithAuto(VentaResponse):
    auto: AutoResponse

# Enums para estados y combustibles
class EstadoAuto(str, Enum):
    DISPONIBLE = "disponible"
    VENDIDO = "vendido"
    RESERVADO = "reservado"
    MANTENIMIENTO = "mantenimiento"

class TipoCombustible(str, Enum):
    GASOLINA = "gasolina"
    DIESEL = "diesel"
    ELECTRICO = "electrico"
    HIBRIDO = "hibrido"


# Agregar al final de models.py

class EstadisticasResponse(BaseModel):
    total_autos: int
    autos_disponibles: int
    autos_vendidos: int
    valor_inventario: float
    ingresos_totales: float
    marca_mas_popular: str