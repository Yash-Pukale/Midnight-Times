/** @type {import('tailwindcss').Config} */
module.exports = {
  prefix: "tw-",
  content: ["./src/**/*.{html,js,vue}"],
  theme: {
    extend: {
      colors:{
        primary: '#EFEFEF',
        'custom-orange': '#FF8A00',
        'custom-green': '#00B207'
      }
    },
  },
  plugins: [

  ],
}
