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
      },
      borderRadius: {
        'md': '8px',     // BUTTONS & NAVIGATION
        'lg': '8px',     // BUTTONS & NAVIGATION
        'xl': '10px',    // CARDS
        '2xl': '10px',   // CARDS
        '3xl': '10px',   // CARDS
      }
    },
  },
  plugins: [
    require('@tailwindcss/typography'),
  ],
}
