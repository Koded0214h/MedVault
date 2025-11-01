import axios from 'axios';

const API_BASE_URL = "http://localhost:8000/api";

const api = axios.create({
    baseURL: API_BASE_URL,
    headers: {
        'Content-Type': 'application/json',
    },
});

api.interceptors.request.use(
    (config) => {
        const token = localStorage.getItem('access-token');
        if(token) {
            config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
    },
    (error) => Promise.reject(error)
);

api.interceptors.response.use(
    (response) => response,
    async (error) => {
        if(error.response?.status === 401) {
            const refreshToken = localStorage.getItem('refresh-token');
            if(refreshToken) {
                try {
                    const response = await axios.post(`${API_BASE_URL}/token/refresh/`, {
                        refresh: refreshToken,
                    });
                    localStorage.setItem('access_token', response.data.access);
                    error.config.headers.Authorization  = `Bearer ${response.data.access}`;
                    return axios(error.config);
                } catch(refreshError) {
                    localStorage.removeItem('access-token');
                    localStorage.removeItem('refresh-token');
                    window.location.href = '/login';
                }
            }
        }
        return Promise.reject(error);
        }
);

export default api;