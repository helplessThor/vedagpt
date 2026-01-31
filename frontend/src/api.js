import axios from 'axios';

const api = axios.create({
    baseURL: import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000', // Configurable for Prod, Default to Local
});

export const chatWithVedaGPT = async (message, history = []) => {
    try {
        const response = await api.post('/chat', { message, history });
        return response.data;
    } catch (error) {
        console.error("API Error Detailed:", error.response || error.message);
        throw error;
    }
};
