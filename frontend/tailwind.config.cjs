/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}", // include all JS/TS/React files
  ],
  theme: {
    extend: {},
  },
  plugins: [],
  // If you are on Tailwind v2.x, you can use:
  // purge: false, // optional
};
