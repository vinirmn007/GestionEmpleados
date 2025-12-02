import React, { useState } from 'react';

const PayrollDetail: React.FC = () => {
  const [expandedId, setExpandedId] = useState<number | null>(null);

  const toggleExpand = (id: number) => {
    setExpandedId(expandedId === id ? null : id);
  };

  const details = [
    { name: 'Ana Martínez', gross: '$2,500.00', deductions: '$350.00', net: '$2,150.00', status: 'Pendiente' },
    { name: 'Carlos Rodríguez', gross: '$3,200.00', deductions: '$480.00', net: '$2,720.00', status: 'Pendiente' },
    { name: 'Laura Gómez', gross: '$2,800.00', deductions: '$410.00', net: '$2,390.00', status: 'Pagado' },
    { name: 'Javier Pérez', gross: '$4,500.00', deductions: '$750.00', net: '$3,750.00', status: 'Error' },
  ];

  return (
    <div className="flex flex-col gap-6">
      <div className="flex flex-wrap justify-between items-center gap-4">
        <div>
          <h1 className="text-3xl font-black text-slate-900 dark:text-white">Detalle de Roles de Pago</h1>
          <p className="text-slate-500 dark:text-slate-400 mt-1">Selecciona los roles que deseas procesar.</p>
        </div>
        <button className="w-full sm:w-auto flex items-center justify-center gap-2 bg-primary text-white px-5 py-2.5 rounded-lg font-bold hover:bg-primary/90 transition-colors shadow-sm">
          <span className="material-symbols-outlined">send</span>
          Enviar al Gestor
        </button>
      </div>

      <div className="bg-white dark:bg-surface-dark rounded-xl border border-slate-200 dark:border-slate-800 p-4 shadow-sm">
        {/* Filters */}
        <div className="flex flex-wrap justify-between items-center gap-4 mb-4">
          <div className="flex gap-2 overflow-x-auto pb-2 md:pb-0 w-full md:w-auto">
            <button className="shrink-0 bg-slate-100 dark:bg-slate-800 px-4 py-2 rounded-lg text-sm font-medium hover:bg-slate-200 dark:hover:bg-slate-700 transition-colors text-slate-700 dark:text-slate-200 flex items-center gap-2">
              Período: Junio 2024 <span className="material-symbols-outlined text-base">expand_more</span>
            </button>
            <button className="shrink-0 bg-slate-100 dark:bg-slate-800 px-4 py-2 rounded-lg text-sm font-medium hover:bg-slate-200 dark:hover:bg-slate-700 transition-colors text-slate-700 dark:text-slate-200 flex items-center gap-2">
              Departamento: Todos <span className="material-symbols-outlined text-base">expand_more</span>
            </button>
            <button className="shrink-0 bg-slate-100 dark:bg-slate-800 px-4 py-2 rounded-lg text-sm font-medium hover:bg-slate-200 dark:hover:bg-slate-700 transition-colors text-slate-700 dark:text-slate-200 flex items-center gap-2">
              Estado: Pendiente <span className="material-symbols-outlined text-base">expand_more</span>
            </button>
          </div>
          <div className="relative w-full md:w-auto">
            <span className="material-symbols-outlined absolute left-3 top-1/2 -translate-y-1/2 text-slate-400">search</span>
            <input type="text" placeholder="Buscar empleado..." className="pl-10 pr-4 py-2 rounded-lg border border-slate-300 dark:border-slate-700 bg-transparent focus:ring-2 focus:ring-primary/50 outline-none w-full md:w-64 text-sm text-slate-900 dark:text-white" />
          </div>
        </div>

        {/* Desktop Table */}
        <div className="hidden md:block overflow-x-auto rounded-lg border border-slate-200 dark:border-slate-800">
          <table className="w-full text-sm">
            <thead className="bg-slate-50 dark:bg-slate-800/50 text-slate-500 dark:text-slate-400 font-medium">
              <tr>
                <th className="p-4 w-10 text-center"><input type="checkbox" className="rounded border-slate-300 text-primary focus:ring-primary/50" /></th>
                <th className="px-4 py-3 text-left">Empleado</th>
                <th className="px-4 py-3 text-left">Período</th>
                <th className="px-4 py-3 text-right">Sueldo Bruto</th>
                <th className="px-4 py-3 text-right">Deducciones</th>
                <th className="px-4 py-3 text-right">Sueldo Neto</th>
                <th className="px-4 py-3 text-left">Estado</th>
                <th className="px-4 py-3 text-center">Acciones</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100 dark:divide-slate-800">
              {details.map((row, idx) => (
                <tr key={idx} className="hover:bg-slate-50 dark:hover:bg-slate-800/50 transition-colors">
                  <td className="p-4 text-center"><input type="checkbox" className="rounded border-slate-300 text-primary focus:ring-primary/50" /></td>
                  <td className="px-4 py-3 font-medium text-slate-900 dark:text-white">{row.name}</td>
                  <td className="px-4 py-3 text-slate-500 dark:text-slate-400">Junio 2024</td>
                  <td className="px-4 py-3 text-right text-slate-500 dark:text-slate-400">{row.gross}</td>
                  <td className="px-4 py-3 text-right text-slate-500 dark:text-slate-400">{row.deductions}</td>
                  <td className="px-4 py-3 text-right font-semibold text-slate-900 dark:text-white">{row.net}</td>
                  <td className="px-4 py-3">
                    <span className={`inline-flex items-center gap-1.5 px-2 py-1 rounded-full text-xs font-medium ${
                      row.status === 'Pagado' ? 'bg-green-100 text-green-700 dark:bg-green-900/30 dark:text-green-300' :
                      row.status === 'Pendiente' ? 'bg-amber-100 text-amber-700 dark:bg-amber-900/30 dark:text-amber-300' :
                      'bg-red-100 text-red-700 dark:bg-red-900/30 dark:text-red-300'
                    }`}>
                      <span className={`size-1.5 rounded-full ${
                        row.status === 'Pagado' ? 'bg-green-500' :
                        row.status === 'Pendiente' ? 'bg-amber-500' : 'bg-red-500'
                      }`}></span>
                      {row.status}
                    </span>
                  </td>
                  <td className="px-4 py-3 text-center">
                    <button className="p-1.5 text-slate-400 hover:text-slate-600 dark:hover:text-slate-200 transition-colors">
                      <span className="material-symbols-outlined text-xl">more_vert</span>
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        {/* Mobile List */}
        <div className="md:hidden flex flex-col divide-y divide-slate-200 dark:divide-slate-800">
          {details.map((row, idx) => (
            <div key={idx} className="py-4">
              <div 
                className="flex items-center justify-between cursor-pointer"
                onClick={() => toggleExpand(idx)}
              >
                <div className="flex items-center gap-3">
                  <input type="checkbox" className="rounded border-slate-300 text-primary focus:ring-primary/50" onClick={(e) => e.stopPropagation()} />
                  <div className="flex flex-col">
                    <span className="font-semibold text-slate-900 dark:text-white">{row.name}</span>
                    <span className="text-xs text-slate-500 dark:text-slate-400 font-medium">Neto: {row.net}</span>
                  </div>
                </div>
                <div className="flex items-center gap-3">
                  <span className={`inline-flex items-center gap-1 px-2 py-0.5 rounded-full text-[10px] font-medium ${
                      row.status === 'Pagado' ? 'bg-green-100 text-green-700 dark:bg-green-900/30 dark:text-green-300' :
                      row.status === 'Pendiente' ? 'bg-amber-100 text-amber-700 dark:bg-amber-900/30 dark:text-amber-300' :
                      'bg-red-100 text-red-700 dark:bg-red-900/30 dark:text-red-300'
                    }`}>
                    {row.status}
                  </span>
                  <span className={`material-symbols-outlined text-slate-400 transition-transform duration-200 ${expandedId === idx ? 'rotate-180' : ''}`}>
                    expand_more
                  </span>
                </div>
              </div>

              <div className={`grid transition-all duration-300 ease-in-out overflow-hidden ${expandedId === idx ? 'grid-rows-[1fr] opacity-100 mt-4' : 'grid-rows-[0fr] opacity-0'}`}>
                <div className="min-h-0 flex flex-col gap-2 text-sm bg-slate-50 dark:bg-slate-800/50 p-3 rounded-lg">
                  <div className="flex justify-between">
                    <span className="text-slate-500 dark:text-slate-400">Bruto:</span>
                    <span className="text-slate-900 dark:text-white font-medium">{row.gross}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-slate-500 dark:text-slate-400">Deducciones:</span>
                    <span className="text-slate-900 dark:text-white font-medium">{row.deductions}</span>
                  </div>
                  <div className="flex justify-end pt-2 mt-2 border-t border-slate-200 dark:border-slate-700">
                    <button className="p-2 text-slate-500 dark:text-slate-400 hover:bg-slate-200 dark:hover:bg-slate-700 rounded-lg">
                      <span className="material-symbols-outlined text-lg">more_horiz</span>
                    </button>
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

export default PayrollDetail;