"""
Constantes de negocio para el sistema de nómina.

Estas constantes centralizan los valores fijos del negocio para evitar
números mágicos dispersos en el código.
"""

# Porcentaje de seguro social obligatorio (deducción)
SEGURO_SOCIAL_PORCENTAJE: float = 0.04

# Umbral de antigüedad para bono de empleado permanente (años)
ANTIGUEDAD_BONO_ANOS: float = 5.0

# Porcentaje de bono por antigüedad
BONO_ANTIGUEDAD_PORCENTAJE: float = 0.10

# Bono de alimentación para empleados permanentes
BONO_ALIMENTACION: float = 1_000_000

# Horas regulares en semana laboral
HORAS_REGULARES_SEMANA: int = 40

# Multiplicador para horas extras
MULTIPLICADOR_HORAS_EXTRAS: float = 1.5

# Umbral de ventas para bono de comisión
VENTAS_BONO_COMISION: float = 20_000_000

# Porcentaje de bono por ventas altas
BONO_VENTAS_PORCENTAJE: float = 0.03

# Porcentaje de fondo de ahorro para empleados por horas
FONDO_AHORRO_PORCENTAJE: float = 0.02

# Umbral de antigüedad para fondo de ahorro (años)
ANTIGUEDAD_FONDO_AHORRO_ANOS: float = 1.0
