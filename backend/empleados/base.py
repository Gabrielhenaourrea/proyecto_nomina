"""
Empleado Asalariado - Implementación de empleado con salario fijo mensual.

Este tipo de empleado recibe un salario mensual fijo más beneficios
adicionales basados en antigüedad y permanencia en la empresa.

Principio S (Single Responsibility): Esta clase solo maneja la lógica
específica del empleado asalariado, delega el cálculo de nómina a la
clase base.
"""

from datetime import date

from empleados.base import Empleado
from empleados.constantes import (
    ANTIGUEDAD_BONO_ANOS,
    BONO_ANTIGUEDAD_PORCENTAJE,
    BONO_ALIMENTACION,
)


class EmpleadoAsalariado(Empleado):
    """
    Empleado con salario mensual fijo.
    
    Recibe un salario mensual predefinido más bonos por antigüedad
    (después de 5 años) y beneficios de alimentación.
    
    Attributes:
        salario_mensual: Monto del salario mensual fijo.
    """
    
    def __init__(
        self,
        nombre: str,
        fecha_ingreso: date,
        salario_mensual: float
    ) -> None:
        """
        Inicializa un empleado asalariado.
        
        Args:
            nombre: Nombre del empleado.
            fecha_ingreso: Fecha de ingreso a la empresa.
            salario_mensual: Salario mensual fijo (debe ser > 0).
            
        Raises:
            ValueError: Si el salario mensual es menor o igual a cero.
        """
        super().__init__(nombre, fecha_ingreso)
        
        if salario_mensual <= 0:
            raise ValueError(
                f"El salario mensual debe ser mayor a 0, recibido: {salario_mensual}"
            )
        
        self._salario_mensual: float = salario_mensual
    
    @property
    def salario_mensual(self) -> float:
        """Retorna el salario mensual del empleado."""
        return self._salario_mensual
    
    @property
    def tipo_empleado(self) -> str:
        """Retorna el tipo de empleado para la API."""
        return "asalariado"
    
    def calcular_salario_bruto(self) -> float:
        """
        Calcula el salario bruto del empleado asalariado.
        
        El salario bruto es simplemente el salario mensual fijo.
        
        Returns:
            Salario mensual del empleado.
        """
        return self._salario_mensual
    
    def calcular_bonos(self) -> float:
        """
        Calcula el bono por antigüedad del empleado.
        
        Aplica un bono del 10% sobre el salario si el empleado
        tiene más de 5 años en la empresa.
        
        Returns:
            Bono de antigüedad o 0 si no aplica.
        """
        if self.anios_en_empresa > ANTIGUEDAD_BONO_ANOS:
            return self._salario_mensual * BONO_ANTIGUEDAD_PORCENTAJE
        return 0.0
    
    def calcular_beneficios(self) -> float:
        """
        Calcula los beneficios del empleado asalariado.
        
        Incluye el bono de alimentación fijo para empleados permanentes.
        
        Returns:
            Monto total de beneficios (bono de alimentación).
        """
        return BONO_ALIMENTACION
