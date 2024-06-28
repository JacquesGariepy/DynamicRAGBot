import api from './api';

export const getDocuments = async () => {
    const response = await api.get('/documents');
    return response.data;
};

export const addDocument = async (content, metadata) => {
    const response = await api.post('/documents', { content, metadata });
    return response.data;
};

export const deleteDocument = async (documentId) => {
    const response = await api.delete(`/documents/${documentId}`);
    return response.data;
};