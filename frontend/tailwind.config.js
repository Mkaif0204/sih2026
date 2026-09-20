/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        canvas: "#09090b",
        surface: {
          DEFAULT: "rgba(24, 24, 27, 0.5)",
          card: "rgba(24, 24, 27, 0.65)",
          hover: "rgba(39, 39, 42, 0.6)",
        },
        border: {
          DEFAULT: "rgba(39, 39, 42, 0.8)",
          subtle: "rgba(63, 63, 70, 0.4)",
        },
        primary: {
          DEFAULT: "#4f46e5",
          hover: "#4338ca",
          muted: "rgba(79, 70, 229, 0.12)",
        }
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', '-apple-system', 'BlinkMacSystemFont', 'Segoe UI', 'Roboto', 'sans-serif'],
      },
    },
  },
  plugins: [],
}
