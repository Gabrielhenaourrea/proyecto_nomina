# Sistema de Nómina

Sistema completo de gestión de nómina desarrollado con FastAPI (Python) y React, siguiendo principios SOLID.

## Estructura del Proyecto

```
nomina/
├── backend/                  # API REST con FastAPI
│   ├── empleados/            # Clases de empleados
│   │   ├── __init__.py
│   │   ├── base.py          # Clase abstracta Empleado
│   │   ├── asalariado.py    # EmpleadoAsalariado
│   │   ├── por_horas.py     # EmpleadoPorHoras
│   │   ├── comision.py      # EmpleadoPorComision
│   │   ├── temporal.py      # EmpleadoTemporal
│   │   └── constantes.py    # Constantes de negocio
│   ├── tests/               # Pruebas unitarias
│   │   ├── __init__.py
│   │   └── test_nomina.py   # 20+ pruebas
│   ├── main.py              # Aplicación FastAPI
│   └── requirements.txt     # Dependencias Python
├── frontend/                # Aplicación React
│   └── src/
│       └── App.jsx          # Interfaz de usuario
└── README.md
```

## Tipos de Empleados

| Tipo | Descripción |
|------|-------------|
| **Asalariado** | Salario mensual fijo + bono por antigüedad (5+ años) + bono alimentación |
| **Por Horas** | Tarifa por hora + horas extras (1.5x) + fondo ahorro opcional |
| **Por Comisión** | Salario base + % comisión + bono si ventas > 20M |
| **Temporal** | Salario fijo sin beneficios adicionales |

## Cálculo de Nómina

```
Salario Neto = Salario Bruto + Bonos + Beneficios - Deducciones (4%)
```

## Instalación y Ejecución

### Backend

```bash
# Instalar dependencias
cd backend
pip install -r requirements.txt

# Ejecutar servidor de desarrollo
uvicorn main:app --reload

# Ejecutar pruebas con cobertura
pytest tests/ -v --cov=empleados --cov-report=term-missing
```

El backend estará disponible en: http://localhost:8000
Documentación Swagger: http://localhost:8000/docs

### Frontend

```bash
# En la carpeta frontend (requiere npm/vite)
cd frontend
npm install
npm run dev
```

El frontend estará disponible en: http://localhost:5173

## Endpoints API

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/` | Mensaje de bienvenida |
| POST | `/nomina/asalariado` | Calcular nómina asalariado |
| POST | `/nomina/por-horas` | Calcular nómina por horas |
| POST | `/nomina/comision` | Calcular nómina por comisión |
| POST | `/nomina/temporal` | Calcular nómina temporal |

## Principio SOLID Aplicados

- **S** (Single Responsibility): Cada clase tiene una sola responsabilidad
- **O** (Open/Closed): Extensible sin modificar código existente
- **L** (Liskov Substitution): Cualquier subclase puede reemplazar a Empleado
- **I** (Interface Segregation): Métodos abstractos separados por responsabilidad
- **D** (Dependency Inversion): FastAPI depende de abstracciones

## Tecnologías

- **Backend**: Python 3.11, FastAPI, Pydantic v2, pytest
- **Frontend**: React 18, Vite, Tailwind CSS
- **Testing**: pytest, pytest-cov
# proyecto_nomina
