"""
Empleado Por Horas - Implementación de empleado con pago por horas trabajadas.

Este tipo de empleado cobra por hora trabajada con un recargo del 50%
para horas extras (más de 40 horas semanales). Puede optar por un
fondo de ahorro voluntario.

Principio S (Single Responsibility): Esta clase solo maneja la lógica
específica del empleado por horas, delega el cálculo de nómina a la
clase base.
Principio O (Open/Closed): Nuevas reglas de beneficios se agregarían
en constantes sin modificar esta clase.
"""

from datetime import date

from empleados.base import Empleado
from empleados.constantes import (
    HORAS_REGULARES_SEMANA,
    MULTIPLICADOR_HORAS_EXTRAS,
    FONDO_AHORRO_PORCENTAJE,
    ANTIGUEDAD_FONDO_AHORRO_ANOS,
)


class EmpleadoPorHoras(Empleado):
    """
    Empleado que cobra por horas trabajadas.
    
    Cobra una tarifa por hora para horas regulares (hasta 40) y
    un 50% adicional por horas extras. Opcionalmente puede optar
    por un fondo de ahorro del 2% del salario bruto.
    
    Attributes:
        tarifa_por_hora: Tarifa base por hora trabajada.
        horas_trabajadas: Total de horas trabajadas en el período.
        acepta_fondo_ahorro: Indica si el empleado opted por fondo de ahorro.
    """
    
    def __init__(
        self,
        nombre: str,
        fecha_ingreso: date,
        tarifa_por_hora: float,
        horas_trabajadas: float,
        acepta_fondo_ahorro: bool = False
    ) -> None:
        """
        Inicializa un empleado por horas.
        
        Args:
            nombre: Nombre del empleado.
            fecha_ingreso: Fecha de ingreso a la empresa.
            tarifa_por_hora: Tarifa por hora (debe ser > 0).
            horas_trabajadas: Horas trabajadas (debe ser >= 0).
            acepta_fondo_ahorro: Si acepta participar en el fondo de ahorro.
            
        Raises:
            ValueError: Si la tarifa es <= 0 o las horas son negativas.
        """
        super().__init__(nombre, fecha_ingreso)
        
        if tarifa_por_hora <= 0:
            raise ValueError(
                f"La tarifa por hora debe ser mayor a 0, recibido: {tarifa_por_hora}"
            )
        
        if horas_trabajadas < 0:
            raise ValueError(
                f"Las horas trabajadas no pueden ser negativas, recibido: {horas_trabajadas}"
            )
        
        self._tarifa_por_hora: float = tarifa_por_hora
        self._horas_trabajadas: float = horas_trabajadas
        self._acepta_fondo_ahorro: bool = acepta_fondo_ahorro
    
    @property
    def tipo_empleado(self) -> str:
        """Retorna el tipo de empleado para la API."""
        return "por_horas"
    
    def calcular_salario_bruto(self) -> float:
        """
        Calcula el salario bruto del empleado por horas.
        
        Aplica tarifa normal para horas regulares (hasta 40) y
        tarifa * 1.5 para horas extras.
        
        Returns:
            Salario bruto calculado.
        """
        horas_regulares = min(self._horas_trabajadas, HORAS_REGULARES_SEMANA)
        horas_extras = max(0, self._horas_trabajadas - HORAS_REGULARES_SEMANA)
        
        salario_regular = horas_regulares * self._tarifa_por_hora
        salario_extras = horas_extras * self._tarifa_por_hora * MULTIPLICADOR_HORAS_EXTRAS
        
        return salario_regular + salario_extras
    
    def calcular_bonos(self) -> float:
        """
        Calcula los bonos del empleado por horas.
        
        Los empleados por horas no reciben bonos.
        
        Returns:
            Siempre 0.
        """
        return 0.0
    
    def calcular_beneficios(self) -> float:
        """
        Calcula los beneficios del empleado por horas.
        
        Aplica el fondo de ahorro del 2% solo si:
        1. El empleado acepta participar.
        2. Tiene más de 1 año en la empresa.
        
        Returns:
            Monto del fondo de ahorro o 0 si no aplica.
        """
        if (self._acepta_fondo_ahorro and 
            self.anios_en_empresa > ANTIGUEDAD_FONDO_AHORRO_ANOS):
            return self.calcular_salario_bruto() * FONDO_AHORRO_PORCENTAJE
        return 0.0
