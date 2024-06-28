import api from './api';

export const queryRAG = async (question) => {
    const response = await api.post('/rag/query', { question });
    return response.data.response;
};

export const getRAGStats = async () => {
    const response = await api.get('/rag/stats');
    return response.data;
};