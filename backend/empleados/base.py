"""
Clase base abstracta para todos los tipos de empleados.

Esta clase implementa el patrón Template Method para el cálculo de nómina:
define el esqueleto del algoritmo en calcular_nomina() y delega los pasos
concretos a las subclases mediante métodos abstractos.

Principio O (Open/Closed): Las subclases extienden el comportamiento
sin modificar esta clase base.
Principio I (Interface Segregation): Métodos abstractos separados para
cada responsabilidad (salario, bonos, beneficios, deducciones).
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import date
from typing import Optional

from empleados.constantes import SEGURO_SOCIAL_PORCENTAJE


@dataclass
class ResultadoNomina:
    """
    Representa el resultado completo del cálculo de nómina.
    
    Dataclass inmutable que contiene todos los componentes del salario
    para un empleado en un período específico.
    """
    nombre: str
    tipo: str
    salario_bruto: float
    bonos: float
    beneficios: float
    deducciones: float
    salario_neto: float


class Empleado(ABC):
    """
    Clase base abstracta para todos los empleados.
    
    Proporciona la estructura común para calcular la nómina y define
    los métodos abstractos que cada tipo de empleado debe implementar.
    
    Attributes:
        nombre: Nombre completo del empleado.
        fecha_ingreso: Fecha en que el empleado ingresó a la empresa.
        seguro_social_porcentaje: Porcentaje de deducción de seguro social.
    """
    
    def __init__(
        self,
        nombre: str,
        fecha_ingreso: date,
        seguro_social_porcentaje: float = SEGURO_SOCIAL_PORCENTAJE
    ) -> None:
        """
        Inicializa un empleado base.
        
        Args:
            nombre: Nombre del empleado.
            fecha_ingreso: Fecha de ingreso a la empresa.
            seguro_social_porcentaje: Porcentaje de seguro social (default 4%).
        """
        if not nombre or not nombre.strip():
            raise ValueError("El nombre del empleado no puede estar vacío")
        
        self._nombre: str = nombre.strip()
        self._fecha_ingreso: date = fecha_ingreso
        self._seguro_social_porcentaje: float = seguro_social_porcentaje
    
    @property
    def nombre(self) -> str:
        """Retorna el nombre del empleado."""
        return self._nombre
    
    @property
    def fecha_ingreso(self) -> date:
        """Retorna la fecha de ingreso del empleado."""
        return self._fecha_ingreso
    
    @property
    def anios_en_empresa(self) -> float:
        """
        Calcula los años que el empleado lleva en la empresa.
        
        Returns:
            Float con los años completos (puede ser fracciones para meses).
        """
        hoy = date.today()
        diferencia = hoy - self._fecha_ingreso
        return diferencia.days / 365.25
    
    @abstractmethod
    def calcular_salario_bruto(self) -> float:
        """
        Calcula el salario bruto del empleado.
        
        Debe ser implementado por cada subclase según su tipo de pago.
        
        Returns:
            Monto del salario bruto antes de deducciones.
        """
        pass
    
    @abstractmethod
    def calcular_bonos(self) -> float:
        """
        Calcula los bonos correspondientes al empleado.
        
        Cada tipo de empleado tiene reglas diferentes para bonos.
        
        Returns:
            Monto total de bonos.
        """
        pass
    
    @abstractmethod
    def calcular_beneficios(self) -> float:
        """
        Calcula los beneficios adicionales del empleado.
        
        Incluye beneficios como bono de alimentación, fondo de ahorro, etc.
        
        Returns:
            Monto total de beneficios.
        """
        pass
    
    def calcular_deducciones(self, salario_bruto: float) -> float:
        """
        Calcula las deducciones obligatorias del empleado.
        
        Incluye seguro social obligatorio (4% del salario bruto).
        
        Args:
            salario_bruto: Monto del salario bruto para calcular deducciones.
            
        Returns:
            Monto total de deducciones.
        """
        return salario_bruto * self._seguro_social_porcentaje
    
    def calcular_nomina(self) -> ResultadoNomina:
        """
        Calcula la nómina completa del empleado.
        
        Orchestrates el cálculo completo: salario bruto + bonos + beneficios
        - deducciones. Este método sigue el patrón Template Method, llamando
        a los métodos abstractos que cada subclase implementa.
        
        Returns:
            ResultadoNomina con todos los componentes del salario.
            
        Raises:
            ValueError: Si el salario neto resulta negativo.
        """
        salario_bruto = self.calcular_salario_bruto()
        bonos = self.calcular_bonos()
        beneficios = self.calcular_beneficios()
        deducciones = self.calcular_deducciones(salario_bruto)
        salario_neto = salario_bruto + bonos + beneficios - deducciones
        
        if salario_neto < 0:
            raise ValueError(
                f"El salario neto no puede ser negativo. "
                f"Calculado: {salario_neto:.2f}"
            )
        
        return ResultadoNomina(
            nombre=self._nombre,
            tipo=self.__class__.__name__,
            salario_bruto=round(salario_bruto, 2),
            bonos=round(bonos, 2),
            beneficios=round(beneficios, 2),
            deducciones=round(deducciones, 2),
            salario_neto=round(salario_neto, 2)
        )
    
    @property
    @abstractmethod
    def tipo_empleado(self) -> str:
        """Retorna el tipo de empleado como string para la API."""
        pass
