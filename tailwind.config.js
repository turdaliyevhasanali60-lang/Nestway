/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./core/templates/**/*.html",
    "./core/templates/*.html"
  ],
  theme: {
    extend: {
      colors: {
        brand: '#008B8B',
        accent: '#FF5733',
      }
    },
  },
  plugins: [
    require('@tailwindcss/typography'),
  ],
}
