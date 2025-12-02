import React from 'react';

const EmployeeCreate: React.FC = () => {
  return (
    <div className="max-w-4xl mx-auto flex flex-col gap-8">
      <header>
        <h1 className="text-3xl font-black text-slate-900 dark:text-white mb-2">Registrar Nuevo Empleado</h1>
        <p className="text-slate-500 dark:text-slate-400">Complete los siguientes campos para agregar un nuevo miembro al equipo.</p>
      </header>

      <div className="bg-white dark:bg-surface-dark p-8 rounded-xl shadow-sm border border-slate-200 dark:border-slate-800">
        <form className="flex flex-col gap-8">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div className="flex flex-col gap-2">
              <label className="text-sm font-semibold text-slate-900 dark:text-slate-200">Nombre *</label>
              <input 
                type="text" 
                className="w-full rounded-lg border border-slate-300 dark:border-slate-700 bg-background-light dark:bg-background-dark p-3 text-slate-900 dark:text-white focus:ring-2 focus:ring-primary/50 outline-none"
                placeholder="Ingrese el nombre"
              />
            </div>
            <div className="flex flex-col gap-2">
              <label className="text-sm font-semibold text-slate-900 dark:text-slate-200">Apellido *</label>
              <input 
                type="text" 
                className="w-full rounded-lg border border-slate-300 dark:border-slate-700 bg-background-light dark:bg-background-dark p-3 text-slate-900 dark:text-white focus:ring-2 focus:ring-primary/50 outline-none"
                placeholder="Ingrese el apellido"
              />
            </div>
            <div className="flex flex-col gap-2">
              <label className="text-sm font-semibold text-slate-900 dark:text-slate-200">DNI / Documento de Identidad *</label>
              <input 
                type="text" 
                className="w-full rounded-lg border border-slate-300 dark:border-slate-700 bg-background-light dark:bg-background-dark p-3 text-slate-900 dark:text-white focus:ring-2 focus:ring-primary/50 outline-none"
                placeholder="Ingrese el número de documento"
              />
            </div>
            <div className="flex flex-col gap-2">
              <label className="text-sm font-semibold text-slate-900 dark:text-slate-200">Posición / Cargo *</label>
              <select className="w-full rounded-lg border border-slate-300 dark:border-slate-700 bg-background-light dark:bg-background-dark p-3 text-slate-900 dark:text-white focus:ring-2 focus:ring-primary/50 outline-none">
                <option value="">Seleccione una posición</option>
                <option value="dev">Desarrollador</option>
                <option value="design">Diseñador UX/UI</option>
                <option value="pm">Gerente de Proyecto</option>
              </select>
            </div>
          </div>

          <div className="flex justify-end pt-4 border-t border-slate-100 dark:border-slate-800">
            <button className="bg-primary text-white font-bold py-3 px-6 rounded-lg hover:bg-primary/90 transition-colors shadow-md">
              Registrar Empleado
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default EmployeeCreate;