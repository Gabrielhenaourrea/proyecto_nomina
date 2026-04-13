"""
Empleado Temporal - Implementación de empleado con contrato fijo.

Este tipo de empleado tiene un contrato por tiempo definido y no
recibe beneficios adicionales como bono de alimentación o bonos
por antigüedad.

Principio S (Single Responsibility): Esta clase solo maneja la lógica
específica del empleado temporal.
Principio L (Liskov Substitution): Esta subclase puede usarse en
cualquier lugar donde se espere un Empleado.
"""

from datetime import date

from empleados.base import Empleado


class EmpleadoTemporal(Empleado):
    """
    Empleado con contrato temporal de duración fija.
    
    Tiene un salario mensual fijo pero no recibe bonos ni beneficios
    adicionales. Su contrato termina en una fecha específica.
    
    Attributes:
        salario_mensual: Salario mensual fijo.
        fecha_fin_contrato: Fecha de finalización del contrato.
    """
    
    def __init__(
        self,
        nombre: str,
        fecha_ingreso: date,
        salario_mensual: float,
        fecha_fin_contrato: date
    ) -> None:
        """
        Inicializa un empleado temporal.
        
        Args:
            nombre: Nombre del empleado.
            fecha_ingreso: Fecha de inicio del contrato.
            salario_mensual: Salario mensual fijo (debe ser > 0).
            fecha_fin_contrato: Fecha de finalización (debe ser > fecha_ingreso).
            
        Raises:
            ValueError: Si el salario es <= 0 o la fecha fin no es posterior
                       a la fecha de ingreso.
        """
        super().__init__(nombre, fecha_ingreso)
        
        if salario_mensual <= 0:
            raise ValueError(
                f"El salario mensual debe ser mayor a 0, recibido: {salario_mensual}"
            )
        
        if fecha_fin_contrato <= fecha_ingreso:
            raise ValueError(
                f"La fecha de fin de contrato debe ser posterior a la fecha "
                f"de ingreso. Fecha ingreso: {fecha_ingreso}, "
                f"Fecha fin: {fecha_fin_contrato}"
            )
        
        self._salario_mensual: float = salario_mensual
        self._fecha_fin_contrato: date = fecha_fin_contrato
    
    @property
    def tipo_empleado(self) -> str:
        """Retorna el tipo de empleado para la API."""
        return "temporal"
    
    def calcular_salario_bruto(self) -> float:
        """
        Calcula el salario bruto del empleado temporal.
        
        Es simplemente el salario mensual fijo.
        
        Returns:
            Salario mensual del empleado.
        """
        return self._salario_mensual
    
    def calcular_bonos(self) -> float:
        """
        Calcula los bonos del empleado temporal.
        
        Los empleados temporales no reciben bonos.
        
        Returns:
            Siempre 0.
        """
        return 0.0
    
    def calcular_beneficios(self) -> float:
        """
        Calcula los beneficios del empleado temporal.
        
        Los empleados temporales no reciben beneficios adicionales.
        
        Returns:
            Siempre 0.
        """
        return 0.0
