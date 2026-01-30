/** @type {import('tailwindcss').Config} */
export default {
    content: [
        "./index.html",
        "./src/**/*.{js,ts,jsx,tsx}",
    ],
    theme: {
        extend: {
            colors: {
                vedic: {
                    primary: '#FF9933', // Saffron
                    secondary: '#8B4513', // Earthy Brown
                    accent: '#FFD700', // Gold
                    bg: '#1A1A1A', // Dark spiritual background
                    paper: '#2D2D2D', // Dark card
                }
            },
            fontFamily: {
                sans: ['Inter', 'sans-serif'],
                serif: ['Merriweather', 'serif'],
            }
        },
    },
    plugins: [],
}
