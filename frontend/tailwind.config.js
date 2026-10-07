/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        'quest-base': '#F2F0E9', // Recycled paper
        'quest-ink': '#2C3333',   // Archival ink
        'quest-sage': '#4B6344',  // Moss/Eucalyptus
        'quest-earth': '#B3543D', // Terracotta
        'quest-parchment': '#E8DFD0', // Pale contrast
        'quest-leaf': '#88B04B',   // Success green
      },
      fontFamily: {
        display: ['Space Grotesk', 'Outfit', 'sans-serif'],
        mono: ['JetBrains Mono', 'monospace'],
      },
      boxShadow: {
        'ink': '4px 4px 0px #2C3333',
        'ink-sm': '2px 2px 0px #2C3333',
      }
    },
  },
  plugins: [],
}
