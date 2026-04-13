"""
Empleado Por Comisión - Implementación de empleado con salario base más comisión.

Este tipo de empleado recibe un salario base más un porcentaje de
comisión sobre sus ventas. También puede recibir un bono adicional
si las ventas superan un umbral establecido.

Principio S (Single Responsibility): Esta clase solo maneja la lógica
específica del empleado por comisión, delega el cálculo de nómina a la
clase base.
"""

from datetime import date

from empleados.base import Empleado
from empleados.constantes import (
    VENTAS_BONO_COMISION,
    BONO_VENTAS_PORCENTAJE,
    BONO_ALIMENTACION,
)


class EmpleadoPorComision(Empleado):
    """
    Empleado con salario base más comisión por ventas.
    
    Recibe un salario fijo más un porcentaje de las ventas realizadas.
    Si las ventas superan el umbral, recibe un bono adicional.
    
    Attributes:
        salario_base: Salario base mensual fijo.
        porcentaje_comision: Porcentaje de comisión sobre ventas (0 a 1).
        ventas_totales: Total de ventas realizadas en el período.
    """
    
    def __init__(
        self,
        nombre: str,
        fecha_ingreso: date,
        salario_base: float,
        porcentaje_comision: float,
        ventas_totales: float
    ) -> None:
        """
        Inicializa un empleado por comisión.
        
        Args:
            nombre: Nombre del empleado.
            fecha_ingreso: Fecha de ingreso a la empresa.
            salario_base: Salario base mensual (debe ser > 0).
            porcentaje_comision: Porcentaje de comisión (entre 0 y 1).
            ventas_totales: Total de ventas (debe ser >= 0).
            
        Raises:
            ValueError: Si el salario base es <= 0, el porcentaje está
                       fuera de rango, o las ventas son negativas.
        """
        super().__init__(nombre, fecha_ingreso)
        
        if salario_base <= 0:
            raise ValueError(
                f"El salario base debe ser mayor a 0, recibido: {salario_base}"
            )
        
        if porcentaje_comision < 0 or porcentaje_comision > 1:
            raise ValueError(
                f"El porcentaje de comisión debe estar entre 0 y 1, "
                f"recibido: {porcentaje_comision}"
            )
        
        if ventas_totales < 0:
            raise ValueError(
                f"Las ventas totales no pueden ser negativas, "
                f"recibido: {ventas_totales}"
            )
        
        self._salario_base: float = salario_base
        self._porcentaje_comision: float = porcentaje_comision
        self._ventas_totales: float = ventas_totales
    
    @property
    def tipo_empleado(self) -> str:
        """Retorna el tipo de empleado para la API."""
        return "comision"
    
    def calcular_salario_bruto(self) -> float:
        """
        Calcula el salario bruto del empleado por comisión.
        
        Incluye el salario base más la comisión sobre ventas.
        
        Returns:
            Salario bruto (base + comisión).
        """
        comision = self._ventas_totales * self._porcentaje_comision
        return self._salario_base + comision
    
    def calcular_bonos(self) -> float:
        """
        Calcula el bono por ventas del empleado.
        
        Aplica un bono del 3% si las ventas totales superan
        el umbral de 20 millones.
        
        Returns:
            Bono por ventas o 0 si no aplica.
        """
        if self._ventas_totales > VENTAS_BONO_COMISION:
            return self._ventas_totales * BONO_VENTAS_PORCENTAJE
        return 0.0
    
    def calcular_beneficios(self) -> float:
        """
        Calcula los beneficios del empleado por comisión.
        
        Incluye el bono de alimentación fijo para empleados permanentes.
        
        Returns:
            Monto total de beneficios (bono de alimentación).
        """
        return BONO_ALIMENTACION
