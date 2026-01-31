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
                    bg: '#0a090b', // Deep Cosmic Void
                    primary: '#ff8c00', // Agni (Deep Saffron)
                    secondary: '#2a2b36', // Vibhuti (Ash Grey)
                    accent: '#ffd700', // Suvarna (Gold)
                    text: '#f5f5f5', // Prakriti (Light)
                    paper: '#1c1c24', // Darker paper tone for depth
                }
            },
            fontFamily: {
                sans: ['Outfit', 'sans-serif'],
                serif: ['Cormorant Garamond', 'serif'],
            }
        },
    },
    plugins: [],
}
