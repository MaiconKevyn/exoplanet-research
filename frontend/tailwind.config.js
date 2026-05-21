/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        space: {
          dark: '#0A0A2A',
          medium: '#1A1A4A',
          light: '#2A2A6A',
          accent: '#8A2BE2', // Blue Violet
          star: '#FFFFE0',   // Light Yellow
        },
      },
      fontFamily: {
        heading: ['Orbitron', 'sans-serif'],
        body: ['Lato', 'sans-serif'],
      },
    },
  },
  plugins: [],
}