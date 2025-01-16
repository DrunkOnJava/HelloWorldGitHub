/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./src/**/*.{astro,html,js,jsx,md,mdx,svelte,ts,tsx,vue}",
    "./pages/**/*.{html,js}",
    "./templates/**/*.html",
    "./guides/**/*.html",
    "./safety/**/*.html",
    "./compounds/**/*.html",
    "./legal/**/*.html",
    "./resources/**/*.html",
    "./training/**/*.html",
    "./nutrition/**/*.html",
    "./protocols/**/*.html",
    "./health/**/*.html",
    "*.html"
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}
