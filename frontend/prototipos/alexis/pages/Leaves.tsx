import React, { useState } from 'react';

const Leaves: React.FC = () => {
  const [expandedId, setExpandedId] = useState<number | null>(null);

  const toggleExpand = (id: number) => {
    setExpandedId(expandedId === id ? null : id);
  };

  const leaves = [
    { name: 'Ana Torres', type: 'Vacaciones', dates: '20 Nov - 24 Nov, 2023', status: 'Pendiente' },
    { name: 'Carlos Ruiz', type: 'Enfermedad', dates: '25 Oct, 2023', status: 'Aprobado' },
    { name: 'Luisa Fernandez', type: 'Asunto Personal', dates: '30 Oct, 2023', status: 'Denegado' },
  ];

  return (
    <div className="flex flex-col gap-6">
      <div className="flex justify-between items-center gap-4">
        <h1 className="text-3xl font-black text-slate-900 dark:text-white">Gestión de Permisos</h1>
      </div>

      <div className="bg-white dark:bg-surface-dark rounded-xl shadow-sm p-4 sm:p-6 border border-slate-200 dark:border-slate-800">
        <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 mb-6">
          <div className="w-full sm:max-w-md relative">
            <span className="material-symbols-outlined absolute left-3 top-1/2 -translate-y-1/2 text-slate-400">search</span>
            <input 
              className="w-full bg-slate-100 dark:bg-background-dark/50 rounded-lg py-2.5 pl-10 pr-4 outline-none text-slate-900 dark:text-white border-transparent focus:ring-2 focus:ring-primary/50" 
              placeholder="Buscar por empleado o fecha..." 
            />
          </div>
          <div className="flex gap-2 w-full sm:w-auto overflow-x-auto pb-2 sm:pb-0">
            {['Todos', 'Pendiente', 'Aprobado', 'Denegado'].map(f => (
              <button key={f} className={`shrink-0 px-4 py-1.5 rounded-lg text-sm font-medium transition-colors ${f === 'Todos' ? 'bg-primary/10 text-primary' : 'bg-slate-100 dark:bg-slate-800 text-slate-600 dark:text-slate-300 hover:bg-slate-200 dark:hover:bg-slate-700'}`}>
                {f}
              </button>
            ))}
          </div>
        </div>

        {/* Desktop Table */}
        <div className="hidden md:block overflow-x-auto">
          <table className="w-full text-sm text-left">
            <thead className="bg-slate-50 dark:bg-slate-800/50 text-slate-500 dark:text-slate-400 font-medium">
              <tr>
                <th className="px-4 py-3 w-12"><input type="checkbox" className="rounded border-slate-300 text-primary" /></th>
                <th className="px-4 py-3">Empleado</th>
                <th className="px-4 py-3">Tipo</th>
                <th className="px-4 py-3">Fechas</th>
                <th className="px-4 py-3">Estado</th>
                <th className="px-4 py-3">Acciones</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100 dark:divide-slate-800">
              {leaves.map((leave, i) => (
                <React.Fragment key={i}>
                  <tr className="hover:bg-slate-50 dark:hover:bg-slate-800/50 transition-colors">
                    <td className="px-4 py-3 text-center"><input type="checkbox" className="rounded border-slate-300 text-primary" /></td>
                    <td className="px-4 py-3 font-medium text-slate-900 dark:text-white">{leave.name}</td>
                    <td className="px-4 py-3 text-slate-500 dark:text-slate-400">{leave.type}</td>
                    <td className="px-4 py-3 text-slate-500 dark:text-slate-400">{leave.dates}</td>
                    <td className="px-4 py-3">
                      <span className={`inline-flex items-center px-2.5 py-1 rounded-full text-xs font-semibold ${
                        leave.status === 'Pendiente' ? 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900/40 dark:text-yellow-300' :
                        leave.status === 'Aprobado' ? 'bg-green-100 text-green-800 dark:bg-green-900/40 dark:text-green-300' :
                        'bg-red-100 text-red-800 dark:bg-red-900/40 dark:text-red-300'
                      }`}>
                        {leave.status}
                      </span>
                    </td>
                    <td className="px-4 py-3">
                      <div className="flex gap-2">
                        <button className={`flex items-center gap-1 px-2 py-1 rounded text-xs font-semibold transition-colors ${leave.status === 'Aprobado' ? 'opacity-50 cursor-not-allowed bg-green-50 text-green-400' : 'bg-green-50 dark:bg-green-900/20 text-green-600 dark:text-green-400 hover:bg-green-100'}`}>
                          <span className="material-symbols-outlined text-base">check_circle</span> Aprobar
                        </button>
                        <button className={`flex items-center gap-1 px-2 py-1 rounded text-xs font-semibold transition-colors ${leave.status === 'Denegado' ? 'opacity-50 cursor-not-allowed bg-red-50 text-red-400' : 'bg-red-50 dark:bg-red-900/20 text-red-600 dark:text-red-400 hover:bg-red-100'}`}>
                          <span className="material-symbols-outlined text-base">cancel</span> Denegar
                        </button>
                      </div>
                    </td>
                  </tr>
                  {i === 0 && (
                    <tr className="bg-primary/5 dark:bg-primary/10">
                      <td colSpan={6} className="p-4">
                        <p className="text-sm font-semibold mb-2 text-slate-900 dark:text-white">Motivo de la Decisión (Opcional)</p>
                        <textarea className="w-full rounded-lg border border-slate-200 dark:border-slate-700 p-2 text-sm bg-white dark:bg-background-dark/50 text-slate-900 dark:text-white outline-none focus:border-primary" placeholder="Añada un comentario..." rows={2}></textarea>
                        <div className="flex justify-end gap-2 mt-3">
                          <button className="px-3 py-1.5 rounded-lg bg-slate-200 dark:bg-slate-700 text-xs font-bold text-slate-700 dark:text-white">Cancelar</button>
                          <button className="px-3 py-1.5 rounded-lg bg-primary text-xs font-bold text-white">Confirmar Aprobación</button>
                        </div>
                      </td>
                    </tr>
                  )}
                </React.Fragment>
              ))}
            </tbody>
          </table>
        </div>

        {/* Mobile List */}
        <div className="md:hidden flex flex-col divide-y divide-slate-200 dark:divide-slate-800">
          {leaves.map((leave, i) => (
            <div key={i} className="py-4">
              <div 
                className="flex items-center justify-between cursor-pointer"
                onClick={() => toggleExpand(i)}
              >
                <div className="flex flex-col">
                  <span className="font-semibold text-slate-900 dark:text-white">{leave.name}</span>
                  <span className="text-xs text-slate-500 dark:text-slate-400">{leave.type}</span>
                </div>
                <div className="flex items-center gap-3">
                  <span className={`inline-flex items-center px-2.5 py-1 rounded-full text-[10px] font-semibold ${
                        leave.status === 'Pendiente' ? 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900/40 dark:text-yellow-300' :
                        leave.status === 'Aprobado' ? 'bg-green-100 text-green-800 dark:bg-green-900/40 dark:text-green-300' :
                        'bg-red-100 text-red-800 dark:bg-red-900/40 dark:text-red-300'
                      }`}>
                    {leave.status}
                  </span>
                  <span className={`material-symbols-outlined text-slate-400 transition-transform duration-200 ${expandedId === i ? 'rotate-180' : ''}`}>
                    expand_more
                  </span>
                </div>
              </div>

              <div className={`grid transition-all duration-300 ease-in-out overflow-hidden ${expandedId === i ? 'grid-rows-[1fr] opacity-100 mt-4' : 'grid-rows-[0fr] opacity-0'}`}>
                <div className="min-h-0 flex flex-col gap-3">
                  <div className="text-sm bg-slate-50 dark:bg-slate-800/50 p-3 rounded-lg">
                    <p className="text-xs text-slate-500 dark:text-slate-400 mb-1">Fechas Solicitadas</p>
                    <p className="text-slate-900 dark:text-white font-medium">{leave.dates}</p>
                  </div>
                  
                  {/* Expanded detail simulation for first row in mobile */}
                  {i === 0 && (
                    <div className="bg-primary/5 dark:bg-primary/10 p-3 rounded-lg">
                      <p className="text-xs font-semibold mb-2 text-slate-900 dark:text-white">Motivo de la Decisión</p>
                      <textarea className="w-full rounded-lg border border-slate-200 dark:border-slate-700 p-2 text-sm bg-white dark:bg-background-dark/50 text-slate-900 dark:text-white outline-none focus:border-primary mb-3" placeholder="Añada un comentario..." rows={2}></textarea>
                      <div className="flex justify-end gap-2">
                        <button className="px-3 py-1.5 rounded-lg bg-slate-200 dark:bg-slate-700 text-xs font-bold text-slate-700 dark:text-white">Cancelar</button>
                        <button className="px-3 py-1.5 rounded-lg bg-primary text-xs font-bold text-white">Aprobar</button>
                      </div>
                    </div>
                  )}

                  <div className="flex gap-2">
                    <button className="flex-1 flex items-center justify-center gap-1 px-3 py-2 rounded-lg bg-green-50 dark:bg-green-900/20 text-green-700 dark:text-green-300 text-xs font-bold">
                      <span className="material-symbols-outlined text-sm">check_circle</span> Aprobar
                    </button>
                    <button className="flex-1 flex items-center justify-center gap-1 px-3 py-2 rounded-lg bg-red-50 dark:bg-red-900/20 text-red-700 dark:text-red-300 text-xs font-bold">
                      <span className="material-symbols-outlined text-sm">cancel</span> Denegar
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

export default Leaves;