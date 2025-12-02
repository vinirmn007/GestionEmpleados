import React from 'react';

const Schedule: React.FC = () => {
  return (
    <div className="flex flex-col h-full relative">
      <div className="flex flex-wrap justify-between items-center gap-4 mb-6">
        <h1 className="text-3xl font-black text-slate-900 dark:text-white">Gestión de Horarios</h1>
        <button className="flex items-center gap-2 bg-primary text-white px-4 py-2 rounded-lg font-bold hover:bg-primary/90 transition-colors shadow-sm w-full sm:w-auto justify-center">
          <span className="material-symbols-outlined text-base">add</span>
          Añadir Turno
        </button>
      </div>

      <div className="flex flex-wrap justify-between items-center gap-4 border-b border-slate-200 dark:border-slate-800 pb-4 mb-4">
        <div className="flex flex-wrap items-center gap-3 w-full sm:w-auto">
          <button className="flex items-center gap-2 px-3 py-1.5 rounded-lg border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-800 text-sm font-medium hover:bg-slate-50 dark:hover:bg-slate-700 text-slate-700 dark:text-slate-200">
            Todos <span className="material-symbols-outlined text-sm">expand_more</span>
          </button>
          <div className="flex items-center bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-lg p-1 flex-1 sm:flex-none justify-between sm:justify-start">
            <button className="p-1 hover:bg-slate-100 dark:hover:bg-slate-700 rounded"><span className="material-symbols-outlined text-base text-slate-500">chevron_left</span></button>
            <span className="px-3 text-sm font-medium text-slate-700 dark:text-slate-200 text-center">2 - 8 Dic</span>
            <button className="p-1 hover:bg-slate-100 dark:hover:bg-slate-700 rounded"><span className="material-symbols-outlined text-base text-slate-500">chevron_right</span></button>
          </div>
        </div>
        <div className="bg-slate-200 dark:bg-slate-800 p-1 rounded-lg flex text-sm font-medium w-full sm:w-auto">
          <button className="flex-1 sm:flex-none px-4 py-1.5 rounded-md bg-white dark:bg-slate-700 text-slate-900 dark:text-white shadow-sm">Semana</button>
          <button className="flex-1 sm:flex-none px-4 py-1.5 rounded-md text-slate-500 dark:text-slate-400 hover:text-slate-700 dark:hover:text-slate-200">Mes</button>
        </div>
      </div>

      <div className="overflow-x-auto rounded-xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-surface-dark shadow-sm">
        <div className="grid min-w-[1000px]" style={{ gridTemplateColumns: '180px repeat(7, 1fr)' }}>
          {/* Header */}
          <div className="p-3 border-b border-r border-slate-200 dark:border-slate-800 bg-slate-50 dark:bg-slate-900 font-semibold text-sm text-slate-600 dark:text-slate-300 sticky left-0 z-20">Empleado</div>
          {['Lunes 2', 'Martes 3', 'Miércoles 4', 'Jueves 5', 'Viernes 6', 'Sábado 7', 'Domingo 8'].map((day, i) => {
             const [d, n] = day.split(' ');
             const isWeekend = i >= 5;
             return (
              <div key={i} className={`p-3 border-b border-slate-200 dark:border-slate-800 text-center ${isWeekend ? 'bg-blue-50 dark:bg-blue-900/20' : 'bg-slate-50 dark:bg-slate-900'}`}>
                <p className={`text-xs ${isWeekend ? 'text-blue-600 dark:text-blue-400' : 'text-slate-500'}`}>{d}</p>
                <p className={`font-bold ${isWeekend ? 'text-blue-800 dark:text-blue-200' : 'text-slate-800 dark:text-slate-100'}`}>{n}</p>
              </div>
             );
          })}

          {/* Rows */}
          <div className="p-3 border-r border-b border-slate-200 dark:border-slate-800 flex items-center gap-3 sticky left-0 bg-white dark:bg-surface-dark z-20">
            <div className="size-8 rounded-full bg-cover bg-center shrink-0" style={{backgroundImage: 'url("https://lh3.googleusercontent.com/aida-public/AB6AXuDyrF9qyh6Ln2r0Ofzp9Ck1qOLjhK8ySPi7bxw037FPifqdxC3gt4qTXV-6K86FnwRBz5jarVt-8bXDBPFA2Opontcd6Re4s8IE4VHCSL7xl-Wb5rBeDze9-fAIRXTju11Ft0-1L-wZ7JcOiAnFD96wWvXTupIx_4QJd67byFRABZgvqwrKwe9R1p8hGkE_2ur3HQfAXq2u-lM2KEgYT1u6p85ZblKx2Nu8-un_izP5zcwZ5uPHzIIByHko5s8x-_ul3tnv-ySVGx0")'}}></div>
            <div className="min-w-0">
              <p className="text-sm font-medium text-slate-800 dark:text-white truncate">Ana García</p>
              <p className="text-xs text-slate-500 truncate">Ventas</p>
            </div>
          </div>
          {[1, 2, 0, 1, 3, 0, 0].map((shift, i) => (
            <div key={i} className="p-2 border-b border-slate-200 dark:border-slate-800 relative">
              {shift === 1 && (
                <div className="bg-green-100 dark:bg-green-900/40 border-l-4 border-green-500 p-1.5 rounded text-xs cursor-pointer hover:brightness-95">
                  <p className="font-bold text-green-800 dark:text-green-200">09:00 - 17:00</p>
                  <p className="text-green-600 dark:text-green-400">Mañana</p>
                </div>
              )}
              {shift === 2 && (
                <div className="bg-green-100 dark:bg-green-900/40 border-l-4 border-green-500 p-1.5 rounded text-xs cursor-pointer hover:brightness-95">
                  <p className="font-bold text-green-800 dark:text-green-200">09:00 - 17:00</p>
                  <p className="text-green-600 dark:text-green-400">Mañana</p>
                </div>
              )}
              {shift === 3 && (
                <div className="bg-green-100 dark:bg-green-900/40 border-l-4 border-green-500 p-1.5 rounded text-xs cursor-pointer hover:brightness-95">
                  <p className="font-bold text-green-800 dark:text-green-200">09:00 - 13:00</p>
                  <p className="text-green-600 dark:text-green-400">Media</p>
                </div>
              )}
            </div>
          ))}

          {/* Row 2 */}
          <div className="p-3 border-r border-b border-slate-200 dark:border-slate-800 flex items-center gap-3 sticky left-0 bg-slate-50 dark:bg-slate-900/50 z-20">
            <div className="size-8 rounded-full bg-cover bg-center shrink-0" style={{backgroundImage: 'url("https://lh3.googleusercontent.com/aida-public/AB6AXuDC7Ic3WwIlVBpry2FsoZOr4OLhcFritIt-BOfcYijhYy7ACgM0EcyWUeG-KlGo5WSzyxNSxlbroegKjr6D786Gzt_UrXRSYhDReG7Tl_Y3HFgmoesLg2lbFMPn5UeBxGpEPdl4NO1zhjB3cS-ElkVDKXDPDeRfd6N3vRIpUyxnlIIMasbB1Ajlp2L4N81vcxGa4hxqWiL2eCHrcMAE6dJuWzaSRyW1c_hHCpHYN9uMNu7WOftpDIOL8AQ7yHIrNuAjMxRbTaKL4Gc")'}}></div>
            <div className="min-w-0">
              <p className="text-sm font-medium text-slate-800 dark:text-white truncate">Carlos R.</p>
              <p className="text-xs text-slate-500 truncate">Marketing</p>
            </div>
          </div>
          {[0, 1, 1, 1, 0, 0, 2].map((shift, i) => (
            <div key={i} className="p-2 border-b border-slate-200 dark:border-slate-800 bg-slate-50 dark:bg-slate-900/50">
              {shift === 1 && (
                <div className="bg-orange-100 dark:bg-orange-900/40 border-l-4 border-orange-500 p-1.5 rounded text-xs cursor-pointer hover:brightness-95">
                  <p className="font-bold text-orange-800 dark:text-orange-200">14:00 - 22:00</p>
                  <p className="text-orange-600 dark:text-orange-400">Tarde</p>
                </div>
              )}
              {shift === 2 && (
                <div className="bg-red-100 dark:bg-red-900/40 border-l-4 border-red-500 p-1.5 rounded text-xs cursor-pointer hover:brightness-95">
                  <p className="font-bold text-red-800 dark:text-red-200">Ausencia</p>
                  <p className="text-red-600 dark:text-red-400">Médico</p>
                </div>
              )}
            </div>
          ))}
        </div>
      </div>

      <div className="fixed bottom-6 left-1/2 -translate-x-1/2 z-30 flex items-center gap-4 bg-white dark:bg-slate-800/90 backdrop-blur-md p-3 rounded-xl shadow-2xl border border-slate-200 dark:border-slate-700 w-[90%] max-w-sm justify-between">
        <p className="text-sm font-medium text-slate-700 dark:text-slate-200">Cambios pendientes</p>
        <div className="flex gap-2">
          <button className="px-3 py-1.5 rounded-lg bg-slate-200 dark:bg-slate-700 text-slate-800 dark:text-white text-xs font-bold hover:bg-slate-300 dark:hover:bg-slate-600 transition-colors">Descartar</button>
          <button className="px-3 py-1.5 rounded-lg bg-primary text-white text-xs font-bold hover:bg-primary/90 transition-colors">Guardar</button>
        </div>
      </div>
    </div>
  );
};

export default Schedule;