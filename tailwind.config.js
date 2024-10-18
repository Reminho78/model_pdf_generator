/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './app/templates/**/*.html',  // Chemin vers les fichiers HTML dans le dossier 'templates'
    './app/static/**/*.css',      // Chemin vers les fichiers CSS dans 'static'
    './app/**/*.py'               // Si tu utilises des classes dans tes fichiers Python
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}