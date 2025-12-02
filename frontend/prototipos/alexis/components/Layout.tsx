import React, { useState } from 'react';
import { Link, useLocation, useNavigate } from 'react-router-dom';
import { useTheme } from '../ThemeContext';

interface LayoutProps {
  children: React.ReactNode;
}

const Layout: React.FC<LayoutProps> = ({ children }) => {
  const { isDark, toggleTheme } = useTheme();
  const location = useLocation();
  const navigate = useNavigate();
  const [isSidebarOpen, setIsSidebarOpen] = useState(false);

  const isActive = (path: string) => {
    if (path === '/') return location.pathname === '/';
    return location.pathname.startsWith(path);
  };

  const navItems = [
    { icon: 'dashboard', label: 'Dashboard', path: '/' },
    { icon: 'groups', label: 'Empleados', path: '/employees' },
    { icon: 'receipt_long', label: 'Roles de Pago', path: '/payroll' },
    { icon: 'schedule', label: 'Marcaciones', path: '/attendance' },
    { icon: 'calendar_month', label: 'Horarios', path: '/schedule' },
    { icon: 'task_alt', label: 'Permisos', path: '/leaves' },
    { icon: 'bar_chart', label: 'Reportes', path: '/reports' },
    { icon: 'settings', label: 'Configuración', path: '/settings' },
  ];

  const toggleSidebar = () => setIsSidebarOpen(!isSidebarOpen);

  return (
    <div className="flex h-screen w-full overflow-hidden bg-background-light dark:bg-background-dark text-slate-800 dark:text-slate-200">
      
      {/* Mobile Sidebar Overlay */}
      {isSidebarOpen && (
        <div 
          className="fixed inset-0 z-20 bg-black/50 md:hidden transition-opacity"
          onClick={() => setIsSidebarOpen(false)}
        />
      )}

      {/* Sidebar */}
      <aside 
        className={`fixed md:static inset-y-0 left-0 z-30 w-64 flex-col border-r border-slate-200 dark:border-slate-800 bg-white dark:bg-background-dark p-4 transition-transform duration-300 ease-in-out ${
          isSidebarOpen ? 'translate-x-0' : '-translate-x-full md:translate-x-0'
        }`}
      >
        <div className="flex items-center justify-between p-2 mb-6">
          <div className="flex items-center gap-3">
            <div className="size-10 rounded-full bg-primary/10 flex items-center justify-center text-primary">
               <span className="material-symbols-outlined text-2xl">groups</span>
            </div>
            <div className="flex flex-col">
              <h1 className="text-base font-bold leading-normal">HR System</h1>
              <p className="text-slate-500 dark:text-slate-400 text-xs font-normal">Panel de Admin</p>
            </div>
          </div>
          <button onClick={() => setIsSidebarOpen(false)} className="md:hidden text-slate-500">
            <span className="material-symbols-outlined">close</span>
          </button>
        </div>

        <nav className="flex flex-col gap-1 flex-1 overflow-y-auto no-scrollbar">
          {navItems.map((item) => (
            <Link
              key={item.path}
              to={item.path}
              onClick={() => setIsSidebarOpen(false)}
              className={`flex items-center gap-3 px-3 py-2 rounded-lg transition-colors ${
                isActive(item.path)
                  ? 'bg-primary/10 text-primary dark:bg-primary/20 dark:text-primary-300'
                  : 'text-slate-600 dark:text-slate-400 hover:bg-slate-100 dark:hover:bg-slate-800'
              }`}
            >
              <span className={`material-symbols-outlined ${isActive(item.path) ? 'fill' : ''}`}>
                {item.icon}
              </span>
              <p className="text-sm font-medium leading-normal">{item.label}</p>
            </Link>
          ))}
        </nav>

        <div className="mt-auto pt-4 border-t border-slate-200 dark:border-slate-800 flex flex-col gap-1">
          <button
            onClick={() => navigate('/login')}
            className="flex items-center gap-3 px-3 py-2 rounded-lg text-slate-600 dark:text-slate-400 hover:bg-red-50 dark:hover:bg-red-900/10 hover:text-red-600 dark:hover:text-red-400 transition-colors w-full text-left"
          >
            <span className="material-symbols-outlined">logout</span>
            <p className="text-sm font-medium leading-normal">Cerrar Sesión</p>
          </button>
        </div>
      </aside>

      {/* Main Content */}
      <div className="flex-1 flex flex-col overflow-hidden w-full">
        {/* Header */}
        <header className="h-16 flex items-center justify-between px-4 sm:px-6 border-b border-slate-200 dark:border-slate-800 bg-white dark:bg-background-dark/80 backdrop-blur-sm z-10 transition-colors duration-300">
          <div className="flex items-center gap-4">
             <button 
               onClick={toggleSidebar}
               className="md:hidden p-2 -ml-2 text-slate-500 hover:bg-slate-100 dark:hover:bg-slate-800 rounded-lg"
             >
               <span className="material-symbols-outlined">menu</span>
             </button>
          </div>
          
          <div className="flex flex-1 justify-end items-center gap-2 sm:gap-4">
            <button 
              onClick={toggleTheme}
              className="flex size-10 items-center justify-center rounded-full hover:bg-slate-100 dark:hover:bg-slate-800 text-slate-600 dark:text-slate-400 transition-colors"
              title="Toggle Theme"
            >
              <span className="material-symbols-outlined">
                {isDark ? 'light_mode' : 'dark_mode'}
              </span>
            </button>
            <button className="flex size-10 items-center justify-center rounded-full hover:bg-slate-100 dark:hover:bg-slate-800 text-slate-600 dark:text-slate-400 transition-colors">
              <span className="material-symbols-outlined">notifications</span>
            </button>
            <div className="flex items-center gap-3 pl-2 border-l border-slate-200 dark:border-slate-700">
               <div className="text-right hidden sm:block">
                  <p className="text-sm font-semibold">Admin User</p>
                  <p className="text-xs text-slate-500">admin@empresa.com</p>
               </div>
               <div 
                 className="size-9 sm:size-10 rounded-full bg-cover bg-center border border-slate-200 dark:border-slate-700"
                 style={{backgroundImage: 'url("https://lh3.googleusercontent.com/aida-public/AB6AXuDIIHUy482WgHfFT-tF3wXoFjN6FjiBXbBbIdMbJwQkrrLsX68Cz3MybWC5k21DJ667byAudObv6Wal6LOkTIcZEiZKmwRwSpZT4qlC3MwgQkrwuUEyDki6zpR_qk4jTbvzLSz4G8bQjwLQwvBXMLlgEnCTVbWKaTzFugOWkPCYAJIn7M2Du9YxGI-MJnW4rJStCZ-sNhqm5cdfL5rJ79Q5ISeowAgWbXNkf-qnLQcMy2hKtQRMz3JJqORHWnI9HiKvEB6QOJm4McU")'}}
               ></div>
            </div>
          </div>
        </header>

        {/* Page Content */}
        <main className="flex-1 overflow-auto p-4 sm:p-6 lg:p-8 bg-background-light dark:bg-background-dark transition-colors duration-300">
          <div className="mx-auto max-w-7xl animate-fade-in">
            {children}
          </div>
        </main>
      </div>
    </div>
  );
};

export default Layout;