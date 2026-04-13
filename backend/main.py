"""
API de Nómina - FastAPI Backend

Sistema de cálculo de nómina para diferentes tipos de empleados.
Proporciona endpoints REST para calcular salarios, bonos, beneficios
y deducciones.

Principio D (Dependency Inversion): Los endpoints dependen de abstracciones
(las clases de empleados), no de implementaciones concretas.
"""

from datetime import date
from typing import Union

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from empleados import (
    EmpleadoAsalariado,
    EmpleadoPorHoras,
    EmpleadoPorComision,
    EmpleadoTemporal,
    ResultadoNomina,
)


app = FastAPI(
    title="Sistema de Nómina",
    description="API para cálculo de nómina de empleados",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class EmpleadoAsalariadoInput(BaseModel):
    """Schema de entrada para empleado asalariado."""
    nombre: str = Field(..., min_length=1, description="Nombre del empleado")
    fecha_ingreso: date = Field(..., description="Fecha de ingreso a la empresa")
    salario_mensual: float = Field(..., gt=0, description="Salario mensual")


class EmpleadoPorHorasInput(BaseModel):
    """Schema de entrada para empleado por horas."""
    nombre: str = Field(..., min_length=1, description="Nombre del empleado")
    fecha_ingreso: date = Field(..., description="Fecha de ingreso a la empresa")
    tarifa_por_hora: float = Field(..., gt=0, description="Tarifa por hora")
    horas_trabajadas: float = Field(..., ge=0, description="Horas trabajadas")
    acepta_fondo_ahorro: bool = Field(default=False, description="Acepta fondo de ahorro")


class EmpleadoPorComisionInput(BaseModel):
    """Schema de entrada para empleado por comisión."""
    nombre: str = Field(..., min_length=1, description="Nombre del empleado")
    fecha_ingreso: date = Field(..., description="Fecha de ingreso a la empresa")
    salario_base: float = Field(..., gt=0, description="Salario base mensual")
    porcentaje_comision: float = Field(
        ...,
        ge=0,
        le=1,
        description="Porcentaje de comisión (0 a 1)"
    )
    ventas_totales: float = Field(..., ge=0, description="Ventas totales del período")


class EmpleadoTemporalInput(BaseModel):
    """Schema de entrada para empleado temporal."""
    nombre: str = Field(..., min_length=1, description="Nombre del empleado")
    fecha_ingreso: date = Field(..., description="Fecha de inicio del contrato")
    salario_mensual: float = Field(..., gt=0, description="Salario mensual")
    fecha_fin_contrato: date = Field(..., description="Fecha de fin de contrato")


@app.get("/")
async def root():
    """Endpoint de bienvenida."""
    return {
        "mensaje": "Sistema de Nómina API",
        "version": "1.0.0",
        "endpoints": {
            "asalariado": "POST /nomina/asalariado",
            "por_horas": "POST /nomina/por-horas",
            "comision": "POST /nomina/comision",
            "temporal": "POST /nomina/temporal",
        }
    }


def _crear_error_422(detalle: str) -> None:
    """Lanza HTTPException con código 422 para errores de validación."""
    raise HTTPException(status_code=422, detail=detalle)


@app.post("/nomina/asalariado", response_model=ResultadoNomina)
async def calcular_nomina_asalariado(data: EmpleadoAsalariadoInput):
    """
    Calcula la nómina de un empleado asalariado.
    
    Args:
        data: Datos del empleado asalariado.
        
    Returns:
        ResultadoNomina con todos los componentes del salario.
    """
    try:
        empleado = EmpleadoAsalariado(
            nombre=data.nombre,
            fecha_ingreso=data.fecha_ingreso,
            salario_mensual=data.salario_mensual,
        )
        return empleado.calcular_nomina()
    except ValueError as e:
        _crear_error_422(str(e))


@app.post("/nomina/por-horas", response_model=ResultadoNomina)
async def calcular_nomina_por_horas(data: EmpleadoPorHorasInput):
    """
    Calcula la nómina de un empleado por horas.
    
    Args:
        data: Datos del empleado por horas.
        
    Returns:
        ResultadoNomina con todos los componentes del salario.
    """
    try:
        empleado = EmpleadoPorHoras(
            nombre=data.nombre,
            fecha_ingreso=data.fecha_ingreso,
            tarifa_por_hora=data.tarifa_por_hora,
            horas_trabajadas=data.horas_trabajadas,
            acepta_fondo_ahorro=data.acepta_fondo_ahorro,
        )
        return empleado.calcular_nomina()
    except ValueError as e:
        _crear_error_422(str(e))


@app.post("/nomina/comision", response_model=ResultadoNomina)
async def calcular_nomina_comision(data: EmpleadoPorComisionInput):
    """
    Calcula la nómina de un empleado por comisión.
    
    Args:
        data: Datos del empleado por comisión.
        
    Returns:
        ResultadoNomina con todos los componentes del salario.
    """
    try:
        empleado = EmpleadoPorComision(
            nombre=data.nombre,
            fecha_ingreso=data.fecha_ingreso,
            salario_base=data.salario_base,
            porcentaje_comision=data.porcentaje_comision,
            ventas_totales=data.ventas_totales,
        )
        return empleado.calcular_nomina()
    except ValueError as e:
        _crear_error_422(str(e))


@app.post("/nomina/temporal", response_model=ResultadoNomina)
async def calcular_nomina_temporal(data: EmpleadoTemporalInput):
    """
    Calcula la nómina de un empleado temporal.
    
    Args:
        data: Datos del empleado temporal.
        
    Returns:
        ResultadoNomina con todos los componentes del salario.
    """
    try:
        empleado = EmpleadoTemporal(
            nombre=data.nombre,
            fecha_ingreso=data.fecha_ingreso,
            salario_mensual=data.salario_mensual,
            fecha_fin_contrato=data.fecha_fin_contrato,
        )
        return empleado.calcular_nomina()
    except ValueError as e:
        _crear_error_422(str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
