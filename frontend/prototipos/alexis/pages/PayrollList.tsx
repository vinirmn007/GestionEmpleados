import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';

const PayrollList: React.FC = () => {
  const navigate = useNavigate();
  const [expandedId, setExpandedId] = useState<number | null>(null);

  const toggleExpand = (id: number) => {
    setExpandedId(expandedId === id ? null : id);
  };

  const payrolls = [
    { period: 'Mayo 2024', date: '01/06/2024', employees: 150, total: '$250,000.00', status: 'Pagado' },
    { period: 'Abril 2024', date: '01/05/2024', employees: 148, total: '$245,000.00', status: 'Pagado' },
    { period: 'Marzo 2024', date: '01/04/2024', employees: 145, total: '$240,000.00', status: 'Pendiente' },
    { period: 'Febrero 2024', date: '01/03/2024', employees: 142, total: '$235,000.00', status: 'Pagado' },
  ];

  return (
    <div className="flex flex-col gap-6">
      <div className="flex flex-wrap justify-between items-center gap-4">
        <div>
          <h1 className="text-3xl font-black text-slate-900 dark:text-white">Gestión de Roles de Pago</h1>
          <p className="text-slate-500 dark:text-slate-400 mt-1">Inicia aquí la generación masiva de roles.</p>
        </div>
        <button 
          onClick={() => navigate('/payroll/create')}
          className="flex items-center justify-center gap-2 bg-primary text-white px-5 py-2.5 rounded-lg font-bold hover:bg-primary/90 transition-colors shadow-sm w-full sm:w-auto"
        >
          <span className="material-symbols-outlined">add_circle</span>
          Generar Nuevo Rol
        </button>
      </div>

      <div className="bg-white dark:bg-surface-dark rounded-xl border border-slate-200 dark:border-slate-800 p-4 shadow-sm">
        {/* Toolbar */}
        <div className="flex flex-wrap items-center justify-between gap-4 mb-4">
          <div className="flex gap-2 overflow-x-auto pb-2 md:pb-0 w-full md:w-auto">
            {['Estado: Todos', 'Mes: Mayo', 'Año: 2024'].map((label) => (
              <button key={label} className="flex shrink-0 items-center gap-2 bg-slate-100 dark:bg-slate-800 px-4 py-2 rounded-lg text-sm font-medium hover:bg-slate-200 dark:hover:bg-slate-700 transition-colors text-slate-700 dark:text-slate-200">
                {label.includes('Estado') && <span className="material-symbols-outlined text-lg">filter_list</span>}
                {label}
                <span className="material-symbols-outlined text-lg">expand_more</span>
              </button>
            ))}
          </div>
          <div className="relative w-full md:w-auto">
            <span className="material-symbols-outlined absolute left-3 top-1/2 -translate-y-1/2 text-slate-400">search</span>
            <input 
              type="text" 
              placeholder="Buscar..." 
              className="pl-10 pr-4 py-2 rounded-lg border border-slate-300 dark:border-slate-700 bg-transparent focus:ring-2 focus:ring-primary/50 outline-none w-full md:w-64 text-sm text-slate-900 dark:text-white"
            />
          </div>
        </div>

        {/* Desktop Table */}
        <div className="hidden md:block overflow-x-auto rounded-lg border border-slate-200 dark:border-slate-800">
          <table className="w-full text-sm text-left">
            <thead className="bg-slate-50 dark:bg-slate-800/50 text-slate-500 dark:text-slate-400 uppercase text-xs font-semibold">
              <tr>
                <th className="px-6 py-4">Período</th>
                <th className="px-6 py-4">Fecha de Generación</th>
                <th className="px-6 py-4">Nº Empleados</th>
                <th className="px-6 py-4">Monto Total</th>
                <th className="px-6 py-4">Estado</th>
                <th className="px-6 py-4">Acciones</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-200 dark:divide-slate-800">
              {payrolls.map((payroll, idx) => (
                <tr key={idx} className="hover:bg-slate-50 dark:hover:bg-slate-800/50 transition-colors group">
                  <td className="px-6 py-4 font-medium text-slate-900 dark:text-white">{payroll.period}</td>
                  <td className="px-6 py-4 text-slate-500 dark:text-slate-400">{payroll.date}</td>
                  <td className="px-6 py-4 text-slate-500 dark:text-slate-400">{payroll.employees}</td>
                  <td className="px-6 py-4 text-slate-500 dark:text-slate-400">{payroll.total}</td>
                  <td className="px-6 py-4">
                    <span className={`inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-medium ${
                      payroll.status === 'Pagado' 
                        ? 'bg-green-100 text-green-700 dark:bg-green-900/30 dark:text-green-400' 
                        : 'bg-yellow-100 text-yellow-700 dark:bg-yellow-900/30 dark:text-yellow-400'
                    }`}>
                      <span className={`size-2 rounded-full ${payroll.status === 'Pagado' ? 'bg-green-500' : 'bg-yellow-500'}`}></span>
                      {payroll.status}
                    </span>
                  </td>
                  <td className="px-6 py-4">
                    <div className="flex gap-2 opacity-0 group-hover:opacity-100 transition-opacity">
                      <button 
                        onClick={() => navigate('/payroll/detail')}
                        className="p-1 hover:text-primary transition-colors" title="Ver detalles"
                      >
                        <span className="material-symbols-outlined text-xl">visibility</span>
                      </button>
                      <button className="p-1 hover:text-primary transition-colors" title="Descargar reporte">
                        <span className="material-symbols-outlined text-xl">download</span>
                      </button>
                      <button className="p-1 hover:text-red-500 transition-colors" title="Eliminar">
                        <span className="material-symbols-outlined text-xl">delete</span>
                      </button>
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        {/* Mobile List */}
        <div className="md:hidden flex flex-col divide-y divide-slate-200 dark:divide-slate-800">
          {payrolls.map((payroll, idx) => (
            <div key={idx} className="py-4">
              <div 
                className="flex items-center justify-between cursor-pointer"
                onClick={() => toggleExpand(idx)}
              >
                <div className="flex flex-col">
                  <span className="font-semibold text-slate-900 dark:text-white">{payroll.period}</span>
                  <span className="text-xs text-slate-500 dark:text-slate-400">{payroll.total}</span>
                </div>
                <div className="flex items-center gap-3">
                  <span className={`inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-medium ${
                      payroll.status === 'Pagado' 
                        ? 'bg-green-100 text-green-700 dark:bg-green-900/30 dark:text-green-400' 
                        : 'bg-yellow-100 text-yellow-700 dark:bg-yellow-900/30 dark:text-yellow-400'
                    }`}>
                    {payroll.status}
                  </span>
                  <span className={`material-symbols-outlined text-slate-400 transition-transform duration-200 ${expandedId === idx ? 'rotate-180' : ''}`}>
                    expand_more
                  </span>
                </div>
              </div>

              <div className={`grid transition-all duration-300 ease-in-out overflow-hidden ${expandedId === idx ? 'grid-rows-[1fr] opacity-100 mt-4' : 'grid-rows-[0fr] opacity-0'}`}>
                <div className="min-h-0 flex flex-col gap-2 text-sm bg-slate-50 dark:bg-slate-800/50 p-3 rounded-lg">
                  <div className="flex justify-between">
                    <span className="text-slate-500 dark:text-slate-400">Fecha:</span>
                    <span className="text-slate-900 dark:text-white">{payroll.date}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-slate-500 dark:text-slate-400">Empleados:</span>
                    <span className="text-slate-900 dark:text-white">{payroll.employees}</span>
                  </div>
                  <div className="flex justify-end gap-3 mt-2 pt-2 border-t border-slate-200 dark:border-slate-700">
                    <button onClick={() => navigate('/payroll/detail')} className="text-slate-600 dark:text-slate-300 hover:text-primary"><span className="material-symbols-outlined">visibility</span></button>
                    <button className="text-slate-600 dark:text-slate-300 hover:text-primary"><span className="material-symbols-outlined">download</span></button>
                    <button className="text-slate-600 dark:text-slate-300 hover:text-red-500"><span className="material-symbols-outlined">delete</span></button>
                  </div>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default PayrollList;