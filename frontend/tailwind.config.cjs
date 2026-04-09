/** @type {import('tailwindcss').Config} */
module.exports = {
  darkMode: ["class"],
  content: ["./index.html", "./src/**/*.{ts,tsx}"],
  theme: {
    extend: {
      colors: {
        background: "#020617",
        foreground: "#e2e8f0",
        card: "rgba(15,23,42,0.85)",
        cardBorder: "rgba(148,163,184,0.25)"
      },
      borderRadius: {
        xl: "1rem"
      },
      boxShadow: {
        glass: "0 18px 45px rgba(15,23,42,0.65)"
      },
      backdropBlur: {
        glass: "18px"
      }
    }
  },
  plugins: []
};

