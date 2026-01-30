import axios from 'axios';

const api = axios.create({
    baseURL: 'http://127.0.0.1:8000', // Use explicit IPv4 for Windows compatibility
});

export const chatWithVedaGPT = async (message) => {
    try {
        const response = await api.post('/chat', { message });
        return response.data;
    } catch (error) {
        console.error("API Error Detailed:", error.response || error.message);
        throw error;
    }
};
