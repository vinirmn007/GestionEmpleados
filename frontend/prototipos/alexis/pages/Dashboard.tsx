import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';

const Dashboard: React.FC = () => {
  const navigate = useNavigate();
  const [expandedId, setExpandedId] = useState<string | null>(null);

  const toggleExpand = (id: string) => {
    setExpandedId(expandedId === id ? null : id);
  };

  const employees = [
    { id: 'EMP-001', name: 'Ana García Pérez', dept: 'Tecnología', role: 'Desarrollador Senior', status: 'Activo', img: 'https://lh3.googleusercontent.com/aida-public/AB6AXuBW1_9pYnT0ScjLRBvHNxjydl2_9yGLfDKzeJUroNKt6AjhUOlAVANbaK8JNrT-cxoH9Ov5Yz609VWXQyG1akWLZO-bdk65283M2YQ3L0U23p1bGr1FgckWmfxx-iTx2UbhNyxb9cRKapBTaW_aFNI8_w3KTOTxELuxzgtIv-ciFVAa2Q5KJFJD3D1gTMTcAkDIXTzr18R--vQ8HgukjqIzNsQl8oHEl1XO9WEKMQS-YUSuHaS8NJ3A4FV-goI3ekQK4sHkz5LMADY' },
    { id: 'EMP-002', name: 'Carlos Ruiz', dept: 'Ventas', role: 'Gerente de Ventas', status: 'Activo', img: 'https://lh3.googleusercontent.com/aida-public/AB6AXuC9ddfDRpnp9kKCJdzNc5-0DYDYachuSwSoJ_8ZCbvuUcVsn3vXUj7OaARdADENG-oTkMh04gaMB0fPh6kGp-243C-B8z1dx3TEz6k6QMm5DZyKTkZ1vMRcAVUPOc6Ex3jY6UCN4teT7adAIAlg0GBQ8bCoPwpooWsYiiWSco8HIVzz1I0d5yiHkOV45uSWw7Omx9c-GcLipPbBC-JnZUlTaUDELvvvHn1FU16YwdJwkvL3jRkS5H_dHrUzXV9umBrIEfRl41lWLwc' },
    { id: 'EMP-003', name: 'Laura Martínez', dept: 'Marketing', role: 'Especialista en SEO', status: 'Activo', img: 'https://lh3.googleusercontent.com/aida-public/AB6AXuC9LsyYPe-jf71fndJPTsf3dVw7i2_8bvFozAnYgrgZKmTS0IPAyxv6qHa5jrPYuSy2NmheX6W7RG3yEQjsSP0nyyFsMZlnYz_bIWNzBa2fiiubt_LdCveWWWeapahvGvifV1eY8C3k0uqz1ExJt18w12qltM8ngSevThC-wHC5-0DCqz0zW4znTy35kwpq9dkDliHTw0mojQ9lnp5rxGFLpV-UccQbpMEKLwNYjrech-f7rYf-wt2Eh4QQzqNdJb8AVVv16D6aK68' },
    { id: 'EMP-004', name: 'Javier Fernández', dept: 'Tecnología', role: 'Analista de Datos', status: 'Inactivo', img: 'https://lh3.googleusercontent.com/aida-public/AB6AXuCwTrZJ2XoDfS30JtziMW8JPaTmzGvF06RtPYV7Zb2yq25X20a9mPqaEqnx8ZlteKqeJvZ9sUf4G3QtE8IulBJqh0jRsQvTiUDMPLsFszu3aP6nnbSokHWQaU9tvq_naVFWMJYHU9_f0Q8PLccTTbA0NQJV26c-AdPxAQ_kVZA9HRjZfKZJcI6vU_yke9AcUubGE9GRThxlJdWD7U-FjqN4mRjqmf3QH00qIr8iFR8qeCJJSr_leapbamzNDdgW7JygVxBi5IT-J7I' },
    { id: 'EMP-005', name: 'Sofía López', dept: 'Recursos Humanos', role: 'Reclutadora', status: 'Activo', img: 'https://lh3.googleusercontent.com/aida-public/AB6AXuD_M9sX4tcmt4p-P9ELzv1gYtVA3zZtNQLJ5mG-vG_NrorBJA5uEvdnrXJt5Tp1yXQY9qBcExXbpmzH4JrfBV5eJnJjGkQFFSc3TebeprHc4zurTUHjekaOXf7fXU2PQRhOLAa0ASv69ZFa4bHjCpURw3-7Iyttv-8IHftRw138tLI7oOqY5pkwFAvdWaTwBrVGdXhcS2_y6LcKHq1-BP770TZDa-u9UL9tKnf1hyO5gjNKVTNS2_iHd-ShfJc_Y70XER8g3h7RWyY' },
  ];

  return (
    <div className="flex flex-col gap-6">
      <div className="flex flex-col sm:flex-row flex-wrap justify-between items-start sm:items-center gap-4">
        <h1 className="text-3xl font-extrabold tracking-tight text-slate-900 dark:text-white">Dashboard de Empleados</h1>
        <button 
          onClick={() => navigate('/employees/new')}
          className="flex items-center justify-center gap-2 rounded-lg h-10 px-4 bg-primary text-white text-sm font-bold shadow-md hover:bg-primary/90 transition-colors w-full sm:w-auto"
        >
          <span className="material-symbols-outlined text-xl">add</span>
          <span>Añadir Nuevo Empleado</span>
        </button>
      </div>

      <div className="bg-white dark:bg-surface-dark rounded-xl border border-slate-200 dark:border-slate-800 shadow-sm overflow-hidden">
        {/* Filters */}
        <div className="p-4 border-b border-slate-200 dark:border-slate-800 flex flex-col md:flex-row gap-4">
          <div className="flex-grow">
            <div className="flex w-full items-center rounded-lg bg-slate-100 dark:bg-background-dark px-3 h-10">
              <span className="material-symbols-outlined text-slate-500">search</span>
              <input 
                className="flex-1 bg-transparent border-none focus:ring-0 text-sm px-2 text-slate-900 dark:text-white placeholder:text-slate-500 outline-none" 
                placeholder="Buscar empleados por nombre o ID"
              />
            </div>
          </div>
          <div className="flex gap-2 overflow-x-auto pb-2 md:pb-0">
            {['Departamento', 'Puesto', 'Estado'].map((filter) => (
              <button key={filter} className="flex shrink-0 h-10 items-center gap-2 rounded-lg border border-slate-200 dark:border-slate-700 px-3 text-sm font-medium hover:border-primary/50 bg-white dark:bg-surface-dark whitespace-nowrap text-slate-700 dark:text-slate-300">
                {filter}
                <span className="material-symbols-outlined text-base">expand_more</span>
              </button>
            ))}
          </div>
        </div>

        {/* Desktop Table */}
        <div className="hidden md:block overflow-x-auto">
          <table className="min-w-full text-sm text-left">
            <thead className="bg-slate-50 dark:bg-background-dark/50 text-slate-500 dark:text-slate-400 font-medium">
              <tr>
                <th className="px-4 py-3 w-14"></th>
                <th className="px-4 py-3">Nombre Completo</th>
                <th className="px-4 py-3">ID Empleado</th>
                <th className="px-4 py-3">Departamento</th>
                <th className="px-4 py-3">Puesto</th>
                <th className="px-4 py-3">Estado</th>
                <th className="px-4 py-3 text-right">Acciones</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-200 dark:divide-slate-800">
              {employees.map((emp) => (
                <tr key={emp.id} className="hover:bg-slate-50 dark:hover:bg-slate-800/50 transition-colors">
                  <td className="px-4 py-3">
                    <div className="size-10 rounded-full bg-cover bg-center" style={{backgroundImage: `url('${emp.img}')`}}></div>
                  </td>
                  <td className="px-4 py-3 font-semibold text-slate-900 dark:text-white">{emp.name}</td>
                  <td className="px-4 py-3 text-slate-500 dark:text-slate-400">{emp.id}</td>
                  <td className="px-4 py-3 text-slate-600 dark:text-slate-300">{emp.dept}</td>
                  <td className="px-4 py-3 text-slate-600 dark:text-slate-300">{emp.role}</td>
                  <td className="px-4 py-3">
                    <span className={`inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-medium ${
                      emp.status === 'Activo' 
                        ? 'bg-green-100 text-green-700 dark:bg-green-900/30 dark:text-green-400' 
                        : 'bg-slate-100 text-slate-600 dark:bg-slate-800 dark:text-slate-400'
                    }`}>
                      <span className={`size-1.5 rounded-full ${emp.status === 'Activo' ? 'bg-green-500' : 'bg-slate-500'}`}></span>
                      {emp.status}
                    </span>
                  </td>
                  <td className="px-4 py-3 text-right">
                    <button className="p-1 hover:bg-slate-100 dark:hover:bg-slate-800 rounded text-slate-400 hover:text-slate-600 dark:hover:text-slate-200 transition-colors">
                      <span className="material-symbols-outlined">more_horiz</span>
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        {/* Mobile List (Card View with Expand) */}
        <div className="md:hidden flex flex-col divide-y divide-slate-200 dark:divide-slate-800">
          {employees.map((emp) => (
            <div key={emp.id} className="p-4 hover:bg-slate-50 dark:hover:bg-slate-800/20 transition-colors">
              <div 
                className="flex items-center justify-between cursor-pointer"
                onClick={() => toggleExpand(emp.id)}
              >
                <div className="flex items-center gap-3">
                  <div className="size-10 rounded-full bg-cover bg-center shrink-0" style={{backgroundImage: `url('${emp.img}')`}}></div>
                  <div className="flex flex-col">
                    <span className="font-semibold text-slate-900 dark:text-white text-sm">{emp.name}</span>
                    <span className="text-xs text-slate-500 dark:text-slate-400">{emp.role}</span>
                  </div>
                </div>
                <div className="flex items-center gap-3">
                  <span className={`inline-flex items-center gap-1 px-2 py-0.5 rounded-full text-[10px] font-medium ${
                      emp.status === 'Activo' 
                        ? 'bg-green-100 text-green-700 dark:bg-green-900/30 dark:text-green-400' 
                        : 'bg-slate-100 text-slate-600 dark:bg-slate-800 dark:text-slate-400'
                    }`}>
                    {emp.status}
                  </span>
                  <span className={`material-symbols-outlined text-slate-400 transition-transform duration-200 ${expandedId === emp.id ? 'rotate-180' : ''}`}>
                    expand_more
                  </span>
                </div>
              </div>
              
              <div className={`grid transition-all duration-300 ease-in-out overflow-hidden ${expandedId === emp.id ? 'grid-rows-[1fr] opacity-100 mt-4' : 'grid-rows-[0fr] opacity-0'}`}>
                <div className="min-h-0 flex flex-col gap-2 text-sm">
                  <div className="grid grid-cols-2 gap-4">
                    <div>
                      <p className="text-xs text-slate-500 dark:text-slate-400">ID Empleado</p>
                      <p className="font-medium text-slate-700 dark:text-slate-200">{emp.id}</p>
                    </div>
                    <div>
                      <p className="text-xs text-slate-500 dark:text-slate-400">Departamento</p>
                      <p className="font-medium text-slate-700 dark:text-slate-200">{emp.dept}</p>
                    </div>
                  </div>
                  <div className="pt-2 flex justify-end gap-2 border-t border-slate-100 dark:border-slate-800 mt-2">
                    <button className="px-3 py-1.5 text-xs font-medium bg-slate-100 dark:bg-slate-800 rounded-lg hover:bg-slate-200 dark:hover:bg-slate-700 text-slate-700 dark:text-slate-300">
                      Ver Perfil
                    </button>
                    <button className="px-3 py-1.5 text-xs font-medium bg-primary/10 text-primary rounded-lg hover:bg-primary/20">
                      Editar
                    </button>
                  </div>
                </div>
              </div>
            </div>
          ))}
        </div>

        {/* Pagination */}
        <div className="flex items-center justify-between p-4 border-t border-slate-200 dark:border-slate-800 text-sm text-slate-500 dark:text-slate-400">
          <p>Mostrando 1-5 de 25</p>
          <div className="flex items-center gap-2">
            <button className="size-8 flex items-center justify-center rounded border border-slate-200 dark:border-slate-700 hover:bg-slate-50 dark:hover:bg-slate-800">
              <span className="material-symbols-outlined text-base">chevron_left</span>
            </button>
            <button className="size-8 flex items-center justify-center rounded bg-primary text-white font-medium">1</button>
            <button className="size-8 flex items-center justify-center rounded border border-slate-200 dark:border-slate-700 hover:bg-slate-50 dark:hover:bg-slate-800 hidden sm:flex">2</button>
            <span className="px-1 hidden sm:block">...</span>
            <button className="size-8 flex items-center justify-center rounded border border-slate-200 dark:border-slate-700 hover:bg-slate-50 dark:hover:bg-slate-800">
              <span className="material-symbols-outlined text-base">chevron_right</span>
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;