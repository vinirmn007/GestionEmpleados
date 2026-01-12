/** @type {import('tailwindcss').Config} */
export default {
  // Aquí le decimos a Tailwind qué archivos mirar para generar el CSS
  content: ['./src/**/*.{html,js,svelte,ts}'], 
  
  // ACTIVAR MODO OSCURO POR CLASE
  darkMode: 'class', 

  theme: {
    extend: {},
  },
  plugins: [],
}