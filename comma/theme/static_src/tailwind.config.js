module.exports = {
    content: [
        "../../templates/**/*{.html,}",
        "../../templates/*{.html,}",
        "../../static/js/*.{js,}",
    ],
    theme: {
        extend: {
            fontFamily: {
            'vazirmatn': ['Vazirmatn', 'sans-serif'],
        },
        },
    },
    plugins: [
        require('@tailwindcss/forms'),
        require('@tailwindcss/typography'),
        require('@tailwindcss/aspect-ratio'),
        require('tailwind-scrollbar'),
    ],
    variants: {
        scrollbar: ['rounded']
  }
}