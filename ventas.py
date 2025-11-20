from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session
from typing import List, Optional
from datetime import datetime
from database import get_session
from repository import VentaRepository
import models

router = APIRouter(prefix="/ventas", tags=["Ventas"])

@router.post("/", response_model=models.VentaResponse)
def crear_venta(
    venta: models.VentaCreate, 
    session: Session = Depends(get_session)
):
    """Crear nueva venta"""
    repo = VentaRepository(session)
    try:
        return repo.create(venta)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error interno del servidor")

@router.get("/", response_model=List[models.VentaResponse])
def listar_ventas(
    skip: int = 0,
    limit: int = 100,
    session: Session = Depends(get_session)
):
    """Listar ventas con paginación"""
    repo = VentaRepository(session)
    return repo.get_all(skip, limit)

@router.get("/{venta_id}", response_model=models.VentaResponse)
def obtener_venta(venta_id: int, session: Session = Depends(get_session)):
    """Obtener venta por ID"""
    repo = VentaRepository(session)
    venta = repo.get_by_id(venta_id)
    if not venta:
        raise HTTPException(status_code=404, detail="Venta no encontrada")
    return venta

@router.put("/{venta_id}", response_model=models.VentaResponse)
def actualizar_venta(
    venta_id: int, 
    venta_update: models.VentaUpdate, 
    session: Session = Depends(get_session)
):
    """Actualizar venta"""
    repo = VentaRepository(session)
    venta = repo.update(venta_id, venta_update)
    if not venta:
        raise HTTPException(status_code=404, detail="Venta no encontrada")
    return venta

@router.delete("/{venta_id}")
def eliminar_venta(venta_id: int, session: Session = Depends(get_session)):
    """Eliminar venta"""
    repo = VentaRepository(session)
    success = repo.delete(venta_id)
    if not success:
        raise HTTPException(status_code=404, detail="Venta no encontrada")
    return {"message": "Venta eliminada correctamente"}

@router.get("/auto/{auto_id}", response_model=List[models.VentaResponse])
def ventas_por_auto(auto_id: int, session: Session = Depends(get_session)):
    """Obtener ventas de un auto específico"""
    repo = VentaRepository(session)
    return repo.get_by_auto_id(auto_id)

@router.get("/comprador/{nombre}", response_model=List[models.VentaResponse])
def ventas_por_comprador(nombre: str, session: Session = Depends(get_session)):
    """Obtener ventas por nombre de comprador"""
    repo = VentaRepository(session)
    return repo.get_by_comprador(nombre)

@router.get("/{venta_id}/with-auto", response_model=models.VentaResponseWithAuto)
def venta_con_auto(venta_id: int, session: Session = Depends(get_session)):
    """Obtener venta con información del auto"""
    repo = VentaRepository(session)
    venta = repo.get_by_id(venta_id)
    if not venta:
        raise HTTPException(status_code=404, detail="Venta no encontrada")
    return venta