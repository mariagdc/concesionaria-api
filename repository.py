from sqlmodel import Session, select, func
from typing import List, Optional
from models import Auto, AutoCreate, AutoUpdate, Venta, VentaCreate, VentaUpdate
import re

class AutoRepository:
    def __init__(self, session: Session):
        self.session = session

    def create(self, auto: AutoCreate) -> Auto:
        db_auto = Auto(**auto.dict())
        self.session.add(db_auto)
        self.session.commit()
        self.session.refresh(db_auto)
        return db_auto

    def get_by_id(self, auto_id: int) -> Optional[Auto]:
        return self.session.get(Auto, auto_id)

    def get_all(self, skip: int = 0, limit: int = 100) -> List[Auto]:
        statement = select(Auto).offset(skip).limit(limit)
        return self.session.exec(statement).all()

    def update(self, auto_id: int, auto_update: AutoUpdate) -> Optional[Auto]:
        db_auto = self.session.get(Auto, auto_id)
        if db_auto:
            update_data = auto_update.dict(exclude_unset=True)
            for field, value in update_data.items():
                setattr(db_auto, field, value)
            self.session.add(db_auto)
            self.session.commit()
            self.session.refresh(db_auto)
        return db_auto

    def delete(self, auto_id: int) -> bool:
        auto = self.session.get(Auto, auto_id)
        if auto:
            self.session.delete(auto)
            self.session.commit()
            return True
        return False

    def get_by_chasis(self, numero_chasis: str) -> Optional[Auto]:
        statement = select(Auto).where(Auto.numero_chasis == numero_chasis)
        return self.session.exec(statement).first()

    def search_by_marca_modelo(self, marca: str = None, modelo: str = None) -> List[Auto]:
        statement = select(Auto)
        if marca:
            statement = statement.where(Auto.marca.ilike(f"%{marca}%"))
        if modelo:
            statement = statement.where(Auto.modelo.ilike(f"%{modelo}%"))
        return self.session.exec(statement).all()

class VentaRepository:
    def __init__(self, session: Session):
        self.session = session

    def create(self, venta: VentaCreate) -> Venta:
        # Verificar que el auto existe
        auto = self.session.get(Auto, venta.auto_id)
        if not auto:
            raise ValueError("Auto no encontrado")
        
        db_venta = Venta(**venta.dict())
        self.session.add(db_venta)
        
        # Actualizar estado del auto a "vendido"
        auto.estado = "vendido"
        self.session.add(auto)
        
        self.session.commit()
        self.session.refresh(db_venta)
        return db_venta

    def get_by_id(self, venta_id: int) -> Optional[Venta]:
        return self.session.get(Venta, venta_id)

    def get_all(self, skip: int = 0, limit: int = 100) -> List[Venta]:
        statement = select(Venta).offset(skip).limit(limit)
        return self.session.exec(statement).all()

    def update(self, venta_id: int, venta_update: VentaUpdate) -> Optional[Venta]:
        db_venta = self.session.get(Venta, venta_id)
        if db_venta:
            update_data = venta_update.dict(exclude_unset=True)
            for field, value in update_data.items():
                setattr(db_venta, field, value)
            self.session.add(db_venta)
            self.session.commit()
            self.session.refresh(db_venta)
        return db_venta

    def delete(self, venta_id: int) -> bool:
        venta = self.session.get(Venta, venta_id)
        if venta:
            self.session.delete(venta)
            self.session.commit()
            return True
        return False

    def get_by_auto_id(self, auto_id: int) -> List[Venta]:
        statement = select(Venta).where(Venta.auto_id == auto_id)
        return self.session.exec(statement).all()

    def get_by_comprador(self, nombre: str) -> List[Venta]:
        statement = select(Venta).where(Venta.nombre_comprador.ilike(f"%{nombre}%"))
        return self.session.exec(statement).all()

    def get_ventas_por_fecha(self, fecha_inicio: datetime, fecha_fin: datetime) -> List[Venta]:
        statement = select(Venta).where(
            Venta.fecha_venta >= fecha_inicio,
            Venta.fecha_venta <= fecha_fin
        )
        return self.session.exec(statement).all()
    
    # Agregar al final de repository.py

class EstadisticasRepository:
    def __init__(self, session: Session):
        self.session = session
        self.auto_repo = AutoRepository(session)
        self.venta_repo = VentaRepository(session)

    def obtener_estadisticas_generales(self) -> dict:
        """Obtener estadísticas completas de la concesionaria"""
        
        # Obtener datos
        autos = self.auto_repo.get_all(limit=10000)  # Número alto para obtener todos
        ventas = self.venta_repo.get_all(limit=10000)
        
        # Cálculos básicos
        total_autos = len(autos)
        autos_disponibles = len([auto for auto in autos if auto.estado == "disponible"])
        autos_vendidos = len([auto for auto in autos if auto.estado == "vendido"])
        
        # Valor del inventario
        valor_inventario = sum(auto.precio for auto in autos if auto.estado == "disponible")
        
        # Ingresos totales
        ingresos_totales = sum(venta.precio for venta in ventas)
        
        # Marca más popular
        from collections import Counter
        if autos:
            marcas = [auto.marca for auto in autos]
            marca_counter = Counter(marcas)
            marca_mas_popular = marca_counter.most_common(1)[0][0]
        else:
            marca_mas_popular = "N/A"
            
        # Estadísticas adicionales que podrían ser útiles
        autos_por_marca = Counter([auto.marca for auto in autos])
        autos_por_estado = Counter([auto.estado for auto in autos])
        ventas_por_comprador = Counter([venta.nombre_comprador for venta in ventas])
        
        return {
            "total_autos": total_autos,
            "autos_disponibles": autos_disponibles,
            "autos_vendidos": autos_vendidos,
            "valor_inventario": valor_inventario,
            "ingresos_totales": ingresos_totales,
            "marca_mas_popular": marca_mas_popular,
            "detalles_autos_por_marca": dict(autos_por_marca),
            "detalles_autos_por_estado": dict(autos_por_estado),
            "total_ventas": len(ventas),
            "comprador_frecuente": ventas_por_comprador.most_common(1)[0][0] if ventas_por_comprador else "N/A"
        }
    
    def obtener_estadisticas_ventas(self) -> dict:
        """Estadísticas específicas de ventas"""
        ventas = self.venta_repo.get_all(limit=10000)
        
        if not ventas:
            return {
                "total_ventas": 0,
                "promedio_venta": 0,
                "venta_mas_alta": 0,
                "venta_mas_baja": 0,
                "ingreso_mensual": 0
            }
        
        precios = [venta.precio for venta in ventas]
        
        return {
            "total_ventas": len(ventas),
            "promedio_venta": sum(precios) / len(precios),
            "venta_mas_alta": max(precios),
            "venta_mas_baja": min(precios),
            "ingreso_mensual": sum(precios) / 12  # Promedio mensual aproximado
        }
    

