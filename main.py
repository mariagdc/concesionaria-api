from fastapi import FastAPI
from contextlib import asynccontextmanager
from database import create_db_and_tables
import autos
import ventas
from repository import EstadisticasRepository

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield

app = FastAPI(
    title="API Concesionaria de Autos - UTN",
    description="API completa para gestión de ventas de autos - Programación IV",
    version="2.0.0",
    lifespan=lifespan
)

# Incluir routers
app.include_router(autos.router)
app.include_router(ventas.router)

@app.get("/")
def root():
    return {"message": "API Concesionaria UTN - Programación IV"}

@app.get("/health")
def health_check():
    return {"status": "healthy", "version": "2.0.0"}


@app.get("/estadisticas", response_model=models.EstadisticasResponse, tags=["Estadísticas"])
def obtener_estadisticas(session: Session = Depends(get_session)):
    """Obtener estadísticas generales de la concesionaria"""
    auto_repo = AutoRepository(session)
    venta_repo = VentaRepository(session)
    
    # Obtener todos los autos para cálculos
    autos = auto_repo.get_all(limit=1000)  # Número alto para obtener todos
    
    total_autos = len(autos)
    autos_disponibles = len([auto for auto in autos if auto.estado == "disponible"])
    autos_vendidos = len([auto for auto in autos if auto.estado == "vendido"])
    
    # Valor del inventario (autos disponibles)
    valor_inventario = sum(auto.precio for auto in autos if auto.estado == "disponible")
    
    # Ingresos totales (precio de venta de autos vendidos)
    # Para esto necesitamos las ventas reales
    todas_ventas = venta_repo.get_all(limit=1000)
    ingresos_totales = sum(venta.precio for venta in todas_ventas)
    
    # Marca más popular
    from collections import Counter
    marcas = [auto.marca for auto in autos]
    marca_counter = Counter(marcas)
    marca_mas_popular = marca_counter.most_common(1)[0][0] if marca_counter else "N/A"
    
    return {
        "total_autos": total_autos,
        "autos_disponibles": autos_disponibles,
        "autos_vendidos": autos_vendidos,
        "valor_inventario": valor_inventario,
        "ingresos_totales": ingresos_totales,
        "marca_mas_popular": marca_mas_popular
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)