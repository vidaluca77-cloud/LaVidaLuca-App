/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './src/app/**/*.{js,ts,jsx,tsx,mdx}',
    './src/pages/**/*.{js,ts,jsx,tsx,mdx}',
    './src/components/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  theme: {
    extend: {
      colors: {
        vida: {
          green: '#22c55e',
          earth: '#a3744e', 
          sky: '#7dd3fc',
          warm: '#fbbf24'
        }
      }
    },
  },
  plugins: [],
}
