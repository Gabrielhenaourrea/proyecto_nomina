/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        'amazon-orange': '#FF9900',
        'amazon-yellow': '#FEBD69',
        'amazon-dark': '#131921',
        'amazon-blue': '#007185',
      }
    },
  },
  plugins: [],
}
