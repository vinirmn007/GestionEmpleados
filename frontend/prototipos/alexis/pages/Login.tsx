import React from 'react';
import { useNavigate } from 'react-router-dom';
import { useTheme } from '../ThemeContext';

const Login: React.FC = () => {
  const navigate = useNavigate();
  const { isDark, toggleTheme } = useTheme();

  const handleLogin = (e: React.FormEvent) => {
    e.preventDefault();
    navigate('/');
  };

  return (
    <div className="relative flex min-h-screen w-full flex-col bg-background-light dark:bg-background-dark overflow-x-hidden transition-colors duration-300">
      <div className="absolute top-4 right-4 z-20">
         <button 
            onClick={toggleTheme}
            className="p-2 rounded-full bg-white/10 backdrop-blur-md border border-white/20 text-slate-800 dark:text-white shadow-lg"
         >
            <span className="material-symbols-outlined">{isDark ? 'light_mode' : 'dark_mode'}</span>
         </button>
      </div>
      <div className="flex h-full grow flex-col">
        <div className="flex flex-1 justify-center items-center p-4">
          <div className="layout-content-container flex flex-col w-full max-w-6xl flex-1">
            <div className="grid grid-cols-1 lg:grid-cols-2 min-h-[80vh] w-full bg-white dark:bg-surface-dark shadow-2xl rounded-2xl overflow-hidden border border-slate-200 dark:border-slate-800">
              
              {/* Left Pane */}
              <div className="relative hidden lg:flex flex-col justify-end p-12 bg-gray-100 dark:bg-gray-800/50">
                <div 
                  className="absolute inset-0 bg-center bg-no-repeat bg-cover transition-transform hover:scale-105 duration-[20s]" 
                  style={{backgroundImage: 'url("https://lh3.googleusercontent.com/aida-public/AB6AXuAinkiG9lphFHgXXg-wdscFpEoMpH6GHS0xm_KOl7Wpl7g1CZcEfT9QbBrXFwFPv_cxm1plYL1Qtwgq9czucxNwbtVm_NJVvt6hLXsVTw9ORL8H9hZR_F0Wgb0RZ_lPrwVL8-5_2SQ925psOE-0140bEExFZPWWQ33V0PyCzpg-_7oV-JwnVn_lvzhlIUiZptG5LkcgbaU-W3Rs7dNmkZ1Wnbi-HVNH-evTMOIGJHbNPdfJycx26K94of3EGAtHY-hXcExh9g4Sfbg")'}}
                >
                  <div className="absolute inset-0 bg-gradient-to-t from-black/80 via-black/20 to-transparent"></div>
                </div>
                <div className="relative z-10">
                  <h2 className="text-white text-4xl font-bold leading-tight mb-4">Impulsando el futuro del trabajo, juntos.</h2>
                  <p className="text-white/90 text-lg font-normal leading-relaxed">Nuestra plataforma centraliza la gestión de talento para un crecimiento eficiente.</p>
                </div>
              </div>

              {/* Right Pane */}
              <div className="flex flex-col justify-center w-full p-8 sm:p-12 md:p-16 bg-white dark:bg-surface-dark">
                <div className="w-full max-w-md mx-auto">
                  <div className="flex items-center gap-2 mb-8">
                     <span className="material-symbols-outlined text-primary text-4xl">groups</span>
                     <span className="text-2xl font-bold text-slate-900 dark:text-white">HR System</span>
                  </div>
                  
                  <h1 className="text-slate-900 dark:text-white tracking-tight text-3xl font-bold leading-tight mb-2">Bienvenido de nuevo</h1>
                  <p className="text-slate-500 dark:text-slate-400 text-base mb-8">Inicia sesión en tu cuenta para continuar.</p>
                  
                  <form onSubmit={handleLogin} className="flex flex-col gap-6">
                    <label className="flex flex-col gap-2">
                      <span className="text-slate-900 dark:text-slate-200 text-sm font-medium">Usuario / Email</span>
                      <input 
                        className="w-full rounded-lg border border-slate-300 dark:border-slate-600 bg-white dark:bg-slate-800/50 px-4 py-3 text-slate-900 dark:text-white focus:border-primary focus:ring-2 focus:ring-primary/20 outline-none transition-all"
                        placeholder="Introduce tu usuario o email"
                        type="email"
                        required
                      />
                    </label>
                    
                    <label className="flex flex-col gap-2">
                      <span className="text-slate-900 dark:text-slate-200 text-sm font-medium">Contraseña</span>
                      <div className="relative">
                        <input 
                          className="w-full rounded-lg border border-slate-300 dark:border-slate-600 bg-white dark:bg-slate-800/50 px-4 py-3 text-slate-900 dark:text-white focus:border-primary focus:ring-2 focus:ring-primary/20 outline-none transition-all pr-12"
                          placeholder="Introduce tu contraseña"
                          type="password"
                          required
                        />
                        <button type="button" className="absolute right-4 top-1/2 -translate-y-1/2 text-slate-400 hover:text-slate-600 dark:hover:text-slate-200">
                          <span className="material-symbols-outlined text-xl">visibility</span>
                        </button>
                      </div>
                    </label>

                    <div className="flex justify-end">
                      <a href="#" className="text-sm font-medium text-primary hover:text-primary/80 transition-colors">¿Olvidaste tu contraseña?</a>
                    </div>

                    <button className="w-full rounded-lg bg-primary py-3.5 text-white font-bold hover:bg-primary/90 transition-colors shadow-lg shadow-primary/20 active:scale-[0.98]">
                      Acceder
                    </button>
                  </form>

                  <div className="mt-12 text-center text-xs text-slate-400 dark:text-slate-500">
                    <p>© 2024 HR System Pro. Todos los derechos reservados.</p>
                    <div className="flex justify-center gap-4 mt-2">
                      <a href="#" className="hover:text-primary transition-colors">Términos</a>
                      <a href="#" className="hover:text-primary transition-colors">Privacidad</a>
                    </div>
                  </div>
                </div>
              </div>

            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Login;