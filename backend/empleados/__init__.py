"""
Módulo de empleados - Sistema de Nómina

Contiene las clases de empleados con sus validaciones y cálculos de nómina.
Sigue los principios SOLID para garantizar extensibilidad y mantenibilidad.
"""

from empleados.base import Empleado, ResultadoNomina
from empleados.asalariado import EmpleadoAsalariado
from empleados.por_horas import EmpleadoPorHoras
from empleados.comision import EmpleadoPorComision
from empleados.temporal import EmpleadoTemporal

__all__ = [
    "Empleado",
    "ResultadoNomina",
    "EmpleadoAsalariado",
    "EmpleadoPorHoras",
    "EmpleadoPorComision",
    "EmpleadoTemporal",
]
