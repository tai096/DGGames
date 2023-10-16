/** @type {import('tailwindcss').Config} */
module.exports = {
  // content: ["./templates/**/*.html",
  //   "./products/templates/**/*.html",
  //   "./products/templates/components/**/*.html",
  //   "./auth/templates/**/*.html",
  //   "./general/templates/**/*.html", ],
  content: ["./**/*.html"],
  theme: {
    extend: {
      colors: {
        primaryColor: "#8858ed",
        secondaryColor: "#2b1f41",
        bgColor: "#0e0e0e",
        textColor: "#ffff",
      },
    },
  },
  plugins: [],
}

