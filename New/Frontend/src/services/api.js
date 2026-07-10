import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const api = axios.create({
    baseURL: API_BASE_URL,
    headers: {
        'Content-Type': 'application/json',
    },
})

export const uploadPDF = async (file, onProgress) => {
    const formData = new FormData();
    formData.append('file', file);

    const response = await api.post('/upload/', formData, {
    headers: {
        'Content-Type': 'multipart/form-data',
    },
    onUploadProgress: (progressEvent) => {
        if(onProgress){
            const percentCompleted = Math.round((progressEvent.loaded *100) / progressEvent.total
     );
    onProgress(percentCompleted);
    }
    },
    
    });

    return response.data;
};

export const askQuestion = async (question, sessionId = 'default') => {
    const response = await api.post('/ask/',{
        question,
        session_id: sessionId,

    });
    return response.data;
};

export const getHistory = async (sessionId = 'default') => {
    const response = await api.get('/history/${sessionId}');
    return response.data;
};

export const clearHistory = async (sessionId = 'default') => {
    const response = await api.delete('/history/${sessionId}');
    return response.data;
};

export const listDocuments = async () => {
    const response = await api.get('/upload/list')
    return response.data;
};

export const deleteDocument = async () => {
    const reponse = await api.delete('/upload/${documentName}');
    return response.data;
};

export const healthCheck =  async () => {
    const response = await api.get('/health');
    return response.data;
}