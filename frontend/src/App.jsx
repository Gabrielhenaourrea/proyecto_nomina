import { useState } from 'react'

const API_BASE = 'http://localhost:8000'

const TIPOS_EMPLEADO = [
  { id: 'asalariado', label: 'Asalariado' },
  { id: 'por_horas', label: 'Por Horas' },
  { id: 'comision', label: 'Comisión' },
  { id: 'temporal', label: 'Temporal' },
]

const formatearCOP = (valor) => {
  return new Intl.NumberFormat('es-CO', {
    style: 'currency',
    currency: 'COP',
    minimumFractionDigits: 0,
    maximumFractionDigits: 0,
  }).format(valor)
}

const obtenerFechaActual = () => {
  const hoy = new Date()
  return hoy.toISOString().split('T')[0]
}

const formatearFecha = (fecha) => {
  const date = new Date(fecha)
  return date.toLocaleDateString('es-CO', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
  })
}

function App() {
  const [tipoEmpleado, setTipoEmpleado] = useState(null)
  const [loading, setLoading] = useState(false)
  const [resultado, setResultado] = useState(null)
  const [error, setError] = useState(null)

  const [formData, setFormData] = useState({
    nombre: '',
    fecha_ingreso: '',
    salario_mensual: '',
    tarifa_por_hora: '',
    horas_trabajadas: '',
    acepta_fondo_ahorro: false,
    salario_base: '',
    porcentaje_comision: '',
    ventas_totales: '',
    fecha_fin_contrato: '',
  })

  const handleInputChange = (e) => {
    const { name, value, type, checked } = e.target
    setFormData(prev => ({
      ...prev,
      [name]: type === 'checkbox' ? checked : value
    }))
    setError(null)
  }

  const construirPayload = () => {
    const base = {
      nombre: formData.nombre,
      fecha_ingreso: formData.fecha_ingreso,
    }

    switch (tipoEmpleado) {
      case 'asalariado':
        return {
          ...base,
          salario_mensual: parseFloat(formData.salario_mensual),
        }
      case 'por_horas':
        return {
          ...base,
          tarifa_por_hora: parseFloat(formData.tarifa_por_hora),
          horas_trabajadas: parseFloat(formData.horas_trabajadas),
          acepta_fondo_ahorro: formData.acepta_fondo_ahorro,
        }
      case 'comision':
        return {
          ...base,
          salario_base: parseFloat(formData.salario_base),
          porcentaje_comision: parseFloat(formData.porcentaje_comision),
          ventas_totales: parseFloat(formData.ventas_totales),
        }
      case 'temporal':
        return {
          ...base,
          salario_mensual: parseFloat(formData.salario_mensual),
          fecha_fin_contrato: formData.fecha_fin_contrato,
        }
      default:
        return {}
    }
  }

  const calcularNomina = async () => {
    setLoading(true)
    setError(null)
    setResultado(null)

    const endpoints = {
      asalariado: '/nomina/asalariado',
      por_horas: '/nomina/por-horas',
      comision: '/nomina/comision',
      temporal: '/nomina/temporal',
    }

    try {
      const response = await fetch(`${API_BASE}${endpoints[tipoEmpleado]}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(construirPayload()),
      })

      const data = await response.json()

      if (!response.ok) {
        throw new Error(data.detail || 'Error al calcular la nómina')
      }

      setResultado(data)
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  const reiniciarFormulario = () => {
    setTipoEmpleado(null)
    setResultado(null)
    setError(null)
    setFormData({
      nombre: '',
      fecha_ingreso: '',
      salario_mensual: '',
      tarifa_por_hora: '',
      horas_trabajadas: '',
      acepta_fondo_ahorro: false,
      salario_base: '',
      porcentaje_comision: '',
      ventas_totales: '',
      fecha_fin_contrato: '',
    })
  }

  const obtenerTipoLabel = () => {
    return TIPOS_EMPLEADO.find(t => t.id === tipoEmpleado)?.label || ''
  }

  return (
    <div className="min-h-screen bg-gray-100">
      <header className="bg-amazon-dark text-white py-6 shadow-lg">
        <div className="max-w-4xl mx-auto px-4">
          <h1 className="text-2xl font-bold">Sistema de Nómina</h1>
          <p className="text-gray-300 text-sm mt-1">Cálculo de nómina para empleados</p>
        </div>
      </header>

      <main className="max-w-4xl mx-auto px-4 py-8">
        {!tipoEmpleado ? (
          <div className="bg-white rounded-lg shadow-md p-8">
            <h2 className="text-xl font-semibold text-gray-800 mb-6 text-center">
              Seleccione el tipo de empleado
            </h2>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
              {TIPOS_EMPLEADO.map((tipo) => (
                <button
                  key={tipo.id}
                  onClick={() => setTipoEmpleado(tipo.id)}
                  className="bg-amazon-orange hover:bg-amazon-yellow text-white font-semibold py-4 px-6 rounded-lg shadow transition-all duration-200 hover:scale-105"
                >
                  {tipo.label}
                </button>
              ))}
            </div>
          </div>
        ) : (
          <div className="space-y-6">
            <div className="bg-white rounded-lg shadow-md p-6">
              <div className="flex items-center justify-between mb-6">
                <div>
                  <h2 className="text-xl font-semibold text-gray-800">
                    Empleado {obtenerTipoLabel()}
                  </h2>
                  <p className="text-gray-500 text-sm">
                    Complete los datos del empleado
                  </p>
                </div>
                <button
                  onClick={reiniciarFormulario}
                  className="text-amazon-blue hover:underline text-sm"
                >
                  Cambiar tipo de empleado
                </button>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Nombre *
                  </label>
                  <input
                    type="text"
                    name="nombre"
                    value={formData.nombre}
                    onChange={handleInputChange}
                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-amazon-orange focus:border-transparent"
                    placeholder="Nombre completo"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Fecha de Ingreso *
                  </label>
                  <input
                    type="date"
                    name="fecha_ingreso"
                    value={formData.fecha_ingreso}
                    onChange={handleInputChange}
                    max={obtenerFechaActual()}
                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-amazon-orange focus:border-transparent"
                  />
                </div>

                {tipoEmpleado === 'asalariado' && (
                  <div className="md:col-span-2">
                    <label className="block text-sm font-medium text-gray-700 mb-1">
                      Salario Mensual (COP) *
                    </label>
                    <input
                      type="number"
                      name="salario_mensual"
                      value={formData.salario_mensual}
                      onChange={handleInputChange}
                      min="0"
                      step="1000"
                      className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-amazon-orange focus:border-transparent"
                      placeholder="Ej: 2500000"
                    />
                  </div>
                )}

                {tipoEmpleado === 'por_horas' && (
                  <>
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">
                        Tarifa por Hora (COP) *
                      </label>
                      <input
                        type="number"
                        name="tarifa_por_hora"
                        value={formData.tarifa_por_hora}
                        onChange={handleInputChange}
                        min="0"
                        step="100"
                        className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-amazon-orange focus:border-transparent"
                        placeholder="Ej: 50000"
                      />
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">
                        Horas Trabajadas *
                      </label>
                      <input
                        type="number"
                        name="horas_trabajadas"
                        value={formData.horas_trabajadas}
                        onChange={handleInputChange}
                        min="0"
                        className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-amazon-orange focus:border-transparent"
                        placeholder="Ej: 48"
                      />
                    </div>
                    <div className="md:col-span-2">
                      <label className="flex items-center space-x-3 cursor-pointer">
                        <input
                          type="checkbox"
                          name="acepta_fondo_ahorro"
                          checked={formData.acepta_fondo_ahorro}
                          onChange={handleInputChange}
                          className="w-5 h-5 text-amazon-orange focus:ring-amazon-orange"
                        />
                        <span className="text-sm text-gray-700">
                          Acepta fondo de ahorro (2% del salario si tiene +1 año)
                        </span>
                      </label>
                    </div>
                  </>
                )}

                {tipoEmpleado === 'comision' && (
                  <>
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">
                        Salario Base (COP) *
                      </label>
                      <input
                        type="number"
                        name="salario_base"
                        value={formData.salario_base}
                        onChange={handleInputChange}
                        min="0"
                        step="1000"
                        className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-amazon-orange focus:border-transparent"
                        placeholder="Ej: 2000000"
                      />
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">
                        Porcentaje de Comisión *
                      </label>
                      <input
                        type="number"
                        name="porcentaje_comision"
                        value={formData.porcentaje_comision}
                        onChange={handleInputChange}
                        min="0"
                        max="1"
                        step="0.01"
                        className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-amazon-orange focus:border-transparent"
                        placeholder="Ej: 0.10"
                      />
                    </div>
                    <div className="md:col-span-2">
                      <label className="block text-sm font-medium text-gray-700 mb-1">
                        Ventas Totales (COP) *
                      </label>
                      <input
                        type="number"
                        name="ventas_totales"
                        value={formData.ventas_totales}
                        onChange={handleInputChange}
                        min="0"
                        step="1000"
                        className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-amazon-orange focus:border-transparent"
                        placeholder="Ej: 15000000"
                      />
                    </div>
                  </>
                )}

                {tipoEmpleado === 'temporal' && (
                  <>
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">
                        Salario Mensual (COP) *
                      </label>
                      <input
                        type="number"
                        name="salario_mensual"
                        value={formData.salario_mensual}
                        onChange={handleInputChange}
                        min="0"
                        step="1000"
                        className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-amazon-orange focus:border-transparent"
                        placeholder="Ej: 2000000"
                      />
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">
                        Fecha Fin de Contrato *
                      </label>
                      <input
                        type="date"
                        name="fecha_fin_contrato"
                        value={formData.fecha_fin_contrato}
                        onChange={handleInputChange}
                        min={formData.fecha_ingreso || obtenerFechaActual()}
                        className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-amazon-orange focus:border-transparent"
                      />
                    </div>
                  </>
                )}
              </div>

              <div className="mt-6">
                <button
                  onClick={calcularNomina}
                  disabled={loading}
                  className={`w-full md:w-auto px-8 py-3 rounded-lg font-semibold text-white shadow transition-all duration-200 ${
                    loading
                      ? 'bg-gray-400 cursor-not-allowed'
                      : 'bg-amazon-orange hover:bg-amazon-yellow hover:text-gray-800'
                  }`}
                >
                  {loading ? (
                    <span className="flex items-center justify-center gap-2">
                      <svg className="animate-spin h-5 w-5" viewBox="0 0 24 24">
                        <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" fill="none" />
                        <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
                      </svg>
                      Calculando...
                    </span>
                  ) : (
                    'Calcular Nómina'
                  )}
                </button>
              </div>
            </div>

            {error && (
              <div className="bg-red-50 border border-red-200 rounded-lg p-4">
                <p className="text-red-600 font-medium">Error</p>
                <p className="text-red-500 text-sm mt-1">{error}</p>
              </div>
            )}

            {resultado && (
              <div className="bg-white rounded-lg shadow-md p-6">
                <h3 className="text-lg font-semibold text-gray-800 mb-4 border-b pb-2">
                  Resultado de Nómina
                </h3>
                
                <div className="space-y-3">
                  <div className="flex justify-between items-center py-2 border-b border-gray-100">
                    <span className="text-gray-600">Empleado</span>
                    <span className="font-medium text-gray-800">{resultado.nombre}</span>
                  </div>
                  
                  <div className="flex justify-between items-center py-2 border-b border-gray-100">
                    <span className="text-gray-600">Tipo</span>
                    <span className="inline-block bg-amazon-orange text-white text-xs px-3 py-1 rounded-full">
                      {resultado.tipo.replace('Empleado', '')}
                    </span>
                  </div>
                  
                  <div className="flex justify-between items-center py-2 border-b border-gray-100">
                    <span className="text-gray-600">Salario Bruto</span>
                    <span className="font-medium text-gray-800">
                      {formatearCOP(resultado.salario_bruto)}
                    </span>
                  </div>
                  
                  <div className="flex justify-between items-center py-2 border-b border-gray-100">
                    <span className="text-gray-600">Bonos</span>
                    <span className="font-medium text-green-600">
                      + {formatearCOP(resultado.bonos)}
                    </span>
                  </div>
                  
                  <div className="flex justify-between items-center py-2 border-b border-gray-100">
                    <span className="text-gray-600">Beneficios</span>
                    <span className="font-medium text-green-600">
                      + {formatearCOP(resultado.beneficios)}
                    </span>
                  </div>
                  
                  <div className="flex justify-between items-center py-2 border-b border-gray-100">
                    <span className="text-gray-600">Deducciones (4%)</span>
                    <span className="font-medium text-red-500">
                      - {formatearCOP(resultado.deducciones)}
                    </span>
                  </div>
                  
                  <div className="flex justify-between items-center py-4 bg-amazon-dark rounded-lg px-4 mt-4">
                    <span className="text-white font-semibold text-lg">Salario Neto</span>
                    <span className="text-amazon-yellow font-bold text-2xl">
                      {formatearCOP(resultado.salario_neto)}
                    </span>
                  </div>
                </div>

                <button
                  onClick={() => {
                    setResultado(null)
                    setFormData({
                      nombre: '',
                      fecha_ingreso: '',
                      salario_mensual: '',
                      tarifa_por_hora: '',
                      horas_trabajadas: '',
                      acepta_fondo_ahorro: false,
                      salario_base: '',
                      porcentaje_comision: '',
                      ventas_totales: '',
                      fecha_fin_contrato: '',
                    })
                  }}
                  className="mt-6 w-full py-2 border border-gray-300 rounded-lg text-gray-600 hover:bg-gray-50 transition-colors"
                >
                  Nueva Nómina
                </button>
              </div>
            )}
          </div>
        )}
      </main>

      <footer className="bg-amazon-dark text-gray-400 py-4 mt-auto">
        <div className="max-w-4xl mx-auto px-4 text-center text-sm">
          Sistema de Nómina - {new Date().getFullYear()}
        </div>
      </footer>
    </div>
  )
}

export default App
