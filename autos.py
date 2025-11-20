from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session
from typing import List, Optional
from database import get_session
from repository import AutoRepository
import models

router = APIRouter(prefix="/autos", tags=["Autos"])

@router.post("/", response_model=models.AutoResponse)
def crear_auto(
    auto: models.AutoCreate, 
    session: Session = Depends(get_session)
):
    """Crear nuevo auto"""
    repo = AutoRepository(session)
    try:
        return repo.create(auto)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/", response_model=List[models.AutoResponse])
def listar_autos(
    skip: int = 0,
    limit: int = 100,
    marca: Optional[str] = Query(None),
    modelo: Optional[str] = Query(None),
    session: Session = Depends(get_session)
):
    """Listar autos con filtros"""
    repo = AutoRepository(session)
    if marca or modelo:
        return repo.search_by_marca_modelo(marca, modelo)
    return repo.get_all(skip, limit)

@router.get("/{auto_id}", response_model=models.AutoResponse)
def obtener_auto(auto_id: int, session: Session = Depends(get_session)):
    """Obtener auto por ID"""
    repo = AutoRepository(session)
    auto = repo.get_by_id(auto_id)
    if not auto:
        raise HTTPException(status_code=404, detail="Auto no encontrado")
    return auto

@router.put("/{auto_id}", response_model=models.AutoResponse)
def actualizar_auto(
    auto_id: int, 
    auto_update: models.AutoUpdate, 
    session: Session = Depends(get_session)
):
    """Actualizar auto"""
    repo = AutoRepository(session)
    auto = repo.update(auto_id, auto_update)
    if not auto:
        raise HTTPException(status_code=404, detail="Auto no encontrado")
    return auto

@router.delete("/{auto_id}")
def eliminar_auto(auto_id: int, session: Session = Depends(get_session)):
    """Eliminar auto"""
    repo = AutoRepository(session)
    success = repo.delete(auto_id)
    if not success:
        raise HTTPException(status_code=404, detail="Auto no encontrado")
    return {"message": "Auto eliminado correctamente"}

@router.get("/chasis/{numero_chasis}", response_model=models.AutoResponse)
def buscar_por_chasis(numero_chasis: str, session: Session = Depends(get_session)):
    """Buscar auto por número de chasis"""
    repo = AutoRepository(session)
    auto = repo.get_by_chasis(numero_chasis)
    if not auto:
        raise HTTPException(status_code=404, detail="Auto no encontrado")
    return auto

@router.get("/{auto_id}/with-ventas", response_model=models.AutoResponseWithVentas)
def auto_con_ventas(auto_id: int, session: Session = Depends(get_session)):
    """Obtener auto con sus ventas"""
    repo = AutoRepository(session)
    auto = repo.get_by_id(auto_id)
    if not auto:
        raise HTTPException(status_code=404, detail="Auto no encontrado")
    return auto