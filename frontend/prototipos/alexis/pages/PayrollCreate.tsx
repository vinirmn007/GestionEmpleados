import React from 'react';
import { useNavigate } from 'react-router-dom';

const PayrollCreate: React.FC = () => {
  const navigate = useNavigate();

  return (
    <div className="max-w-4xl mx-auto flex flex-col gap-8">
      <header>
        <h1 className="text-3xl font-bold text-slate-900 dark:text-white">Creación de Rol de Pago</h1>
        <p className="text-slate-500 dark:text-slate-400 mt-1">Seleccione el período para el cual desea generar los roles de pago.</p>
      </header>

      <div className="bg-white dark:bg-surface-dark p-8 rounded-xl border border-slate-200 dark:border-slate-800 shadow-sm">
        <div className="flex flex-col gap-6">
          <div className="flex flex-col gap-2">
            <label className="text-sm font-medium text-slate-900 dark:text-slate-200">Período de Generación</label>
            <div className="relative">
              <span className="material-symbols-outlined absolute left-3 top-1/2 -translate-y-1/2 text-slate-400 text-xl">calendar_month</span>
              <input 
                type="month" 
                defaultValue="2023-10"
                className="w-full rounded-lg border border-slate-300 dark:border-slate-700 bg-background-light dark:bg-background-dark pl-10 pr-4 py-3 text-slate-900 dark:text-white focus:ring-2 focus:ring-primary/50 outline-none"
              />
            </div>
          </div>

          <div className="pt-2">
            <button 
              onClick={() => navigate('/payroll/detail')}
              className="flex items-center justify-center gap-2 bg-primary text-white font-bold py-3 px-6 rounded-lg hover:bg-primary/90 transition-colors w-full sm:w-auto"
            >
              <span className="material-symbols-outlined text-xl">add_circle</span>
              Generar Roles de Pago
            </button>
          </div>
        </div>
      </div>

      <div className="bg-white dark:bg-surface-dark p-6 rounded-xl border border-slate-200 dark:border-slate-800 shadow-sm flex items-start gap-4">
        <div className="size-12 rounded-full bg-primary/10 flex items-center justify-center text-primary shrink-0">
          <span className="material-symbols-outlined text-2xl">info</span>
        </div>
        <div>
          <h3 className="font-semibold text-slate-900 dark:text-white">Información del Proceso</h3>
          <p className="text-sm text-slate-500 dark:text-slate-400 mt-1">Una vez que genere los roles, el proceso se ejecutará en segundo plano. Se le notificará por correo electrónico cuando haya finalizado.</p>
        </div>
      </div>
    </div>
  );
};

export default PayrollCreate;