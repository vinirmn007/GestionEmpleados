import React from 'react';

const Settings: React.FC = () => {
  return (
    <div className="max-w-4xl mx-auto flex flex-col gap-8">
      <div>
        <h1 className="text-3xl font-bold text-slate-900 dark:text-white">Configuración de Nómina</h1>
        <p className="text-slate-500 dark:text-slate-400 mt-1">Estos valores se aplicarán a todos los cálculos de nómina futuros.</p>
      </div>

      <div className="bg-white dark:bg-surface-dark rounded-xl border border-slate-200 dark:border-slate-800 shadow-sm overflow-hidden">
        <div className="px-6 py-4 border-b border-slate-200 dark:border-slate-800">
          <h3 className="font-bold text-lg text-slate-900 dark:text-white">Valores por Hora</h3>
        </div>
        
        <div className="p-6 grid grid-cols-1 md:grid-cols-2 gap-6">
          <div className="space-y-2">
            <label className="text-sm font-medium text-slate-700 dark:text-slate-300">Pago por Hora Normal</label>
            <div className="relative">
              <span className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-500">$</span>
              <input type="number" defaultValue="25.00" className="w-full pl-8 pr-4 py-3 rounded-lg border border-slate-300 dark:border-slate-700 bg-background-light dark:bg-background-dark text-slate-900 dark:text-white focus:ring-2 focus:ring-primary/50 outline-none" />
            </div>
          </div>
          <div className="space-y-2">
            <label className="text-sm font-medium text-slate-700 dark:text-slate-300">Valor Hora Extra</label>
            <div className="relative">
              <span className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-500">$</span>
              <input type="number" defaultValue="37.50" className="w-full pl-8 pr-4 py-3 rounded-lg border border-slate-300 dark:border-slate-700 bg-background-light dark:bg-background-dark text-slate-900 dark:text-white focus:ring-2 focus:ring-primary/50 outline-none" />
            </div>
          </div>
          <div className="space-y-2">
            <label className="text-sm font-medium text-slate-700 dark:text-slate-300">Valor Hora Nocturna</label>
            <div className="relative">
              <span className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-500">$</span>
              <input type="number" defaultValue="30.00" className="w-full pl-8 pr-4 py-3 rounded-lg border border-slate-300 dark:border-slate-700 bg-background-light dark:bg-background-dark text-slate-900 dark:text-white focus:ring-2 focus:ring-primary/50 outline-none" />
            </div>
          </div>
        </div>

        <div className="px-6 py-4 border-t border-b border-slate-200 dark:border-slate-800 bg-slate-50/50 dark:bg-slate-900/20 mt-2">
          <h3 className="font-bold text-lg text-slate-900 dark:text-white">Otros Valores</h3>
        </div>

        <div className="p-6 grid grid-cols-1 md:grid-cols-2 gap-6">
          <div className="space-y-2">
            <label className="text-sm font-medium text-slate-700 dark:text-slate-300">Valor por Atraso (minuto)</label>
            <div className="relative">
              <span className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-500">$</span>
              <input type="number" defaultValue="0.50" className="w-full pl-8 pr-4 py-3 rounded-lg border border-slate-300 dark:border-slate-700 bg-background-light dark:bg-background-dark text-slate-900 dark:text-white focus:ring-2 focus:ring-primary/50 outline-none" />
            </div>
          </div>
          <div className="space-y-2">
            <label className="text-sm font-medium text-slate-700 dark:text-slate-300">Bonificación por Cumplimiento</label>
            <div className="relative">
              <span className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-500">$</span>
              <input type="number" defaultValue="250.00" className="w-full pl-8 pr-4 py-3 rounded-lg border border-slate-300 dark:border-slate-700 bg-background-light dark:bg-background-dark text-slate-900 dark:text-white focus:ring-2 focus:ring-primary/50 outline-none" />
            </div>
          </div>
          <div className="space-y-2">
            <label className="text-sm font-medium text-slate-700 dark:text-slate-300">Deducción por Ausencia (día)</label>
            <div className="relative">
              <span className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-500">$</span>
              <input type="number" defaultValue="200.00" className="w-full pl-8 pr-4 py-3 rounded-lg border border-slate-300 dark:border-slate-700 bg-background-light dark:bg-background-dark text-slate-900 dark:text-white focus:ring-2 focus:ring-primary/50 outline-none" />
            </div>
          </div>
        </div>

        <div className="bg-slate-50 dark:bg-slate-900/50 p-6 flex justify-end gap-4 border-t border-slate-200 dark:border-slate-800">
          <button className="px-6 py-2.5 rounded-lg border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-800 font-semibold text-slate-700 dark:text-slate-300 hover:bg-slate-50 dark:hover:bg-slate-700 transition-colors">Cancelar</button>
          <button className="px-6 py-2.5 rounded-lg bg-primary text-white font-semibold hover:bg-primary/90 transition-colors shadow-sm">Guardar Cambios</button>
        </div>
      </div>
    </div>
  );
};

export default Settings;