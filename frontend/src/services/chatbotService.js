import api from './api';

export const sendChatMessage = async (message, language = 'en') => {
    try {
        const response = await api.post('/chatbot/message', { message, language });
        return response.data.response;
    } catch (error) {
        console.error('Error in sendChatMessage:', error);
        throw error;
    }
};