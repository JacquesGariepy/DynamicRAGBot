import api from './api';

export const getBots = async () => {
    const response = await api.get('/bot');
    return response.data;
};

export const createBot = async (name, config) => {
    const response = await api.post('/bot', { name, config });
    return response.data;
};

export const startBot = async (botId) => {
    const response = await api.post(`/bot/${botId}/start`);
    return response.data;
};

export const stopBot = async (botId) => {
    const response = await api.post(`/bot/${botId}/stop`);
    return response.data;
};

export const deleteBot = async (botId) => {
    const response = await api.delete(`/bot/${botId}`);
    return response.data;
};