// Axios instances for both auth (FastAPI) and django (Django REST)


import axios from 'axios';


// Base URLs are read from environment variables so you can change them per environment
const AUTH_API = process.env.REACT_APP_AUTH_API_URL || 'http://localhost:8000';
const DJANGO_API = process.env.REACT_APP_DJANGO_API_URL || 'http://localhost:8001';


// Axios instance for authentication service (FastAPI)
export const authApi = axios.create({
    baseURL: AUTH_API,
    withCredentials: true, // send/receive cookies (httpOnly cookies)
    headers: {
        'Content-Type': 'application/json'
    }
});


// Axios instance for Django API (products, cart, orders)
export const djangoApi = axios.create({
    baseURL: DJANGO_API,
    withCredentials: true, // include session cookies (Django session)
    headers: {
        'Content-Type': 'application/json'
    }
});


// Optional: simple response interceptor for logging / unified error handling
authApi.interceptors.response.use(
    response => response,
    error => {
        // You can inspect error.response.status and handle globally (e.g., 401)
        return Promise.reject(error);
    }
);


djangoApi.interceptors.response.use(
    response => response,
    error => {
        return Promise.reject(error);
    }
);