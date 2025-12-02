import React, { useState } from 'react';

const Attendance: React.FC = () => {
  const [showModal, setShowModal] = useState(false);
  const [expandedId, setExpandedId] = useState<number | null>(null);

  const toggleExpand = (id: number) => {
    setExpandedId(expandedId === id ? null : id);
  };

  const records = [
    { id: 'EMP-001', name: 'Ana Torres', entry: '09:01 AM', exit: '06:03 PM', hours: '8h 2m', status: 'Completo', type: 'normal' },
    { id: 'EMP-002', name: 'Carlos Vega', entry: '08:55 AM', exit: '05:58 PM', hours: '8h 3m', status: 'Completo', type: 'normal' },
    { id: 'EMP-003', name: 'Luisa Ramos', entry: '09:15 AM', exit: '', hours: '-', status: 'Incompleto', type: 'error' },
    { id: 'EMP-004', name: 'Javier Soto', entry: '09:05 AM', exit: '06:10 PM', hours: '8h 5m', status: 'Editado', type: 'warning' },
    { id: 'EMP-005', name: 'Sofia Reyes', entry: '09:00 AM', exit: '06:00 PM', hours: '8h 0m', status: 'Completo', type: 'normal' },
  ];

  return (
    <div className="flex flex-col gap-6 relative">
      <div className="flex flex-wrap justify-between items-center gap-4">
        <div>
          <h1 className="text-3xl font-black text-slate-900 dark:text-white">Gestión de Marcaciones</h1>
          <p className="text-slate-500 dark:text-slate-400 mt-1">Visualiza y gestiona las marcaciones.</p>
        </div>
        <div className="flex gap-2 w-full sm:w-auto">
          <button className="flex-1 sm:flex-none justify-center px-4 py-2 rounded-lg border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-900 text-slate-700 dark:text-slate-200 font-bold hover:bg-slate-50 dark:hover:bg-slate-800 transition-colors">
            Descartar
          </button>
          <button className="flex-1 sm:flex-none justify-center flex items-center gap-2 px-4 py-2 rounded-lg bg-primary text-white font-bold hover:bg-primary/90 transition-colors">
            <span className="material-symbols-outlined text-base">save</span>
            Guardar
          </button>
        </div>
      </div>

      {/* Toolbar */}
      <div className="flex flex-wrap justify-between gap-4 py-4 items-center bg-white dark:bg-surface-dark p-4 rounded-lg border border-slate-200 dark:border-slate-800">
        <div className="relative flex-grow w-full md:w-auto md:max-w-sm">
          <span className="material-symbols-outlined absolute left-3 top-1/2 -translate-y-1/2 text-slate-400">search</span>
          <input 
            type="text" 
            placeholder="Buscar por empleado..." 
            className="w-full pl-10 pr-4 py-2 rounded-lg border border-slate-300 dark:border-slate-700 bg-transparent focus:ring-2 focus:ring-primary/50 outline-none text-slate-900 dark:text-white"
          />
        </div>
        <div className="flex gap-2 flex-wrap w-full md:w-auto">
          <div className="relative flex-grow md:flex-grow-0">
            <span className="material-symbols-outlined absolute left-3 top-1/2 -translate-y-1/2 text-slate-400">calendar_today</span>
            <input 
              type="date" 
              defaultValue="2024-10-26"
              className="w-full md:w-auto pl-10 pr-4 py-2 rounded-lg border border-slate-300 dark:border-slate-700 bg-transparent focus:ring-2 focus:ring-primary/50 outline-none text-slate-900 dark:text-white"
            />
          </div>
          {['Todos los Departamentos', 'Todos los Estados'].map((opt) => (
            <select key={opt} className="flex-grow md:flex-grow-0 px-4 py-2 rounded-lg border border-slate-300 dark:border-slate-700 bg-transparent focus:ring-2 focus:ring-primary/50 outline-none text-slate-900 dark:text-white">
              <option>{opt}</option>
            </select>
          ))}
        </div>
      </div>

      {/* Desktop Table */}
      <div className="hidden md:block bg-white dark:bg-surface-dark rounded-xl border border-slate-200 dark:border-slate-800 overflow-hidden shadow-sm">
        <div className="overflow-x-auto">
          <table className="w-full text-sm text-left">
            <thead className="bg-slate-50 dark:bg-slate-800/50 text-slate-600 dark:text-slate-400">
              <tr>
                <th className="p-4 w-12 text-center"><input type="checkbox" className="rounded border-slate-300 text-primary focus:ring-primary/50" /></th>
                <th className="px-4 py-3 font-medium">Empleado</th>
                <th className="px-4 py-3 font-medium">ID</th>
                <th className="px-4 py-3 font-medium">Entrada</th>
                <th className="px-4 py-3 font-medium">Salida</th>
                <th className="px-4 py-3 font-medium">Horas</th>
                <th className="px-4 py-3 font-medium">Estado</th>
                <th className="px-4 py-3 font-medium text-center">Acciones</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-200 dark:divide-slate-800">
              {records.map((rec, idx) => (
                <tr 
                  key={idx} 
                  className={`hover:bg-slate-50 dark:hover:bg-slate-800/50 transition-colors
                    ${rec.type === 'error' ? 'bg-red-50/50 dark:bg-red-900/10 border-l-4 border-red-400' : ''}
                    ${rec.type === 'warning' ? 'bg-yellow-50/50 dark:bg-yellow-900/10 border-l-4 border-yellow-400' : ''}
                  `}
                >
                  <td className="p-4 text-center"><input type="checkbox" className="rounded border-slate-300 text-primary focus:ring-primary/50" /></td>
                  <td className="px-4 py-3 font-medium text-slate-900 dark:text-white">{rec.name}</td>
                  <td className="px-4 py-3 text-slate-500 dark:text-slate-400">{rec.id}</td>
                  <td className="px-4 py-3">
                    <input 
                      type="time" 
                      defaultValue={rec.entry.replace(' AM', '').replace(' PM', '')}
                      className="w-24 bg-transparent border border-slate-300 dark:border-slate-700 rounded p-1 text-center text-slate-900 dark:text-white"
                    />
                  </td>
                  <td className="px-4 py-3">
                    <input 
                      type="time" 
                      defaultValue={rec.exit ? rec.exit.replace(' AM', '').replace(' PM', '') : ''}
                      className={`w-24 bg-transparent border rounded p-1 text-center text-slate-900 dark:text-white ${rec.type === 'error' ? 'border-red-400 focus:border-red-500 focus:ring-red-500' : 'border-slate-300 dark:border-slate-700'}`}
                    />
                  </td>
                  <td className="px-4 py-3 text-slate-500 dark:text-slate-400">{rec.hours}</td>
                  <td className="px-4 py-3">
                    <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${
                      rec.status === 'Completo' ? 'bg-green-100 text-green-800 dark:bg-green-900/50 dark:text-green-300' :
                      rec.status === 'Incompleto' ? 'bg-red-100 text-red-800 dark:bg-red-900/50 dark:text-red-300' :
                      'bg-yellow-100 text-yellow-800 dark:bg-yellow-900/50 dark:text-yellow-300'
                    }`}>
                      {rec.status}
                    </span>
                  </td>
                  <td className="px-4 py-3 text-center">
                    <button 
                      onClick={() => setShowModal(true)}
                      className={`hover:bg-slate-200 dark:hover:bg-slate-700 p-1 rounded transition-colors ${rec.type === 'warning' ? 'text-primary' : 'text-slate-500 dark:text-slate-400'}`}
                    >
                      <span className={`material-symbols-outlined text-xl ${rec.type === 'warning' ? 'fill' : ''}`}>
                        {rec.type === 'error' ? 'add_comment' : 'comment'}
                      </span>
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* Mobile List */}
      <div className="md:hidden flex flex-col gap-3">
        {records.map((rec, idx) => (
          <div key={idx} className={`bg-white dark:bg-surface-dark rounded-xl border p-4 shadow-sm ${
            rec.type === 'error' ? 'border-red-400 bg-red-50/50 dark:bg-red-900/10' : 
            rec.type === 'warning' ? 'border-yellow-400 bg-yellow-50/50 dark:bg-yellow-900/10' : 
            'border-slate-200 dark:border-slate-800'
          }`}>
            <div 
              className="flex justify-between items-center cursor-pointer"
              onClick={() => toggleExpand(idx)}
            >
              <div className="flex items-center gap-3">
                <input type="checkbox" className="rounded border-slate-300 text-primary focus:ring-primary/50" onClick={(e) => e.stopPropagation()} />
                <div>
                  <div className="font-bold text-slate-900 dark:text-white">{rec.name}</div>
                  <div className="text-xs text-slate-500 dark:text-slate-400">{rec.id}</div>
                </div>
              </div>
              <div className="flex items-center gap-2">
                <span className={`inline-flex items-center px-2 py-0.5 rounded-full text-[10px] font-medium ${
                  rec.status === 'Completo' ? 'bg-green-100 text-green-800 dark:bg-green-900/50 dark:text-green-300' :
                  rec.status === 'Incompleto' ? 'bg-red-100 text-red-800 dark:bg-red-900/50 dark:text-red-300' :
                  'bg-yellow-100 text-yellow-800 dark:bg-yellow-900/50 dark:text-yellow-300'
                }`}>
                  {rec.status}
                </span>
                <span className={`material-symbols-outlined text-slate-400 transition-transform duration-200 ${expandedId === idx ? 'rotate-180' : ''}`}>expand_more</span>
              </div>
            </div>

            <div className={`grid transition-all duration-300 ease-in-out overflow-hidden ${expandedId === idx ? 'grid-rows-[1fr] opacity-100 mt-4' : 'grid-rows-[0fr] opacity-0'}`}>
              <div className="min-h-0 flex flex-col gap-3">
                <div className="grid grid-cols-2 gap-3">
                  <div>
                    <label className="text-xs text-slate-500 dark:text-slate-400 block mb-1">Entrada</label>
                    <input 
                      type="time" 
                      defaultValue={rec.entry.replace(' AM', '').replace(' PM', '')}
                      className="w-full bg-slate-50 dark:bg-slate-800/50 border border-slate-300 dark:border-slate-700 rounded p-2 text-center text-slate-900 dark:text-white text-sm"
                    />
                  </div>
                  <div>
                    <label className="text-xs text-slate-500 dark:text-slate-400 block mb-1">Salida</label>
                    <input 
                      type="time" 
                      defaultValue={rec.exit ? rec.exit.replace(' AM', '').replace(' PM', '') : ''}
                      className={`w-full bg-slate-50 dark:bg-slate-800/50 border rounded p-2 text-center text-slate-900 dark:text-white text-sm ${rec.type === 'error' ? 'border-red-400' : 'border-slate-300 dark:border-slate-700'}`}
                    />
                  </div>
                </div>
                <div className="flex justify-between items-center pt-2 border-t border-slate-200 dark:border-slate-700/50">
                  <div className="text-sm font-medium text-slate-700 dark:text-slate-300">
                    Total: {rec.hours}
                  </div>
                  <button 
                    onClick={() => setShowModal(true)}
                    className="flex items-center gap-1 text-sm text-primary font-medium hover:underline"
                  >
                    <span className="material-symbols-outlined text-lg">comment</span>
                    Agregar Nota
                  </button>
                </div>
              </div>
            </div>
          </div>
        ))}
      </div>

      {/* Modal */}
      {showModal && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50 backdrop-blur-sm animate-fade-in p-4">
          <div className="bg-white dark:bg-surface-dark rounded-xl shadow-2xl w-full max-w-md overflow-hidden border border-slate-200 dark:border-slate-800">
            <div className="p-6">
              <div className="flex justify-between items-start mb-4">
                <div>
                  <h3 className="text-lg font-bold text-slate-900 dark:text-white">Nota de Edición</h3>
                  <p className="text-sm text-slate-500 dark:text-slate-400">Javier Soto - EMP-004</p>
                </div>
                <button onClick={() => setShowModal(false)} className="text-slate-400 hover:text-slate-600 dark:hover:text-white">
                  <span className="material-symbols-outlined">close</span>
                </button>
              </div>
              <label className="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-2">Motivo:</label>
              <textarea 
                className="w-full rounded-lg border border-slate-300 dark:border-slate-700 bg-background-light dark:bg-background-dark p-3 text-slate-900 dark:text-white focus:ring-2 focus:ring-primary/50 outline-none resize-none"
                rows={4}
                defaultValue="Salida ajustada manualmente."
              ></textarea>
            </div>
            <div className="px-6 py-4 bg-slate-50 dark:bg-slate-800/50 flex justify-end gap-3 border-t border-slate-100 dark:border-slate-800">
              <button 
                onClick={() => setShowModal(false)}
                className="px-4 py-2 rounded-lg border border-slate-300 dark:border-slate-700 text-slate-700 dark:text-slate-300 font-bold hover:bg-slate-50 dark:hover:bg-slate-700 transition-colors"
              >
                Cancelar
              </button>
              <button 
                onClick={() => setShowModal(false)}
                className="px-4 py-2 rounded-lg bg-primary text-white font-bold hover:bg-primary/90 transition-colors"
              >
                Guardar
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default Attendance;