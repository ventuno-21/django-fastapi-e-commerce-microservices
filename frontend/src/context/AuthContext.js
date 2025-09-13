// src/context/AuthContext.js
import React, { createContext, useEffect, useState } from 'react';
import { authApi } from '../api/apiClient';

export const AuthContext = createContext();

export default function AuthProvider({ children }) {
    const [user, setUser] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    // load current user from FastAPI auth service
    const loadUser = async () => {
        try {
            const res = await authApi.get('/me');
            setUser(res.data.user ?? res.data ?? null);
        } catch (err) {
            setUser(null);
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        loadUser();
    }, []);

    const login = async ({ username, password }) => {
        setLoading(true);
        setError(null);
        try {
            // 1. POST login to FastAPI
            const res = await authApi.post('/auth/login', { username, password });

            // 2. set JWT token for future requests
            const token = res.data.access_token;
            authApi.defaults.headers.common['Authorization'] = `Bearer ${token}`;

            // 3. fetch current user
            await loadUser();
        } catch (err) {
            setError(err.response?.data?.detail || 'Login failed');
            throw err;
        } finally {
            setLoading(false);
        }
    };


    // register a new user
    const register = async (data) => {
        setLoading(true);
        setError(null);
        try {
            await authApi.post('/auth/register', data);
            await login({ username: data.username, password: data.password });
        } catch (err) {
            setError(err.response?.data?.detail || 'Register failed');
            throw err;
        } finally {
            setLoading(false);
        }
    };

    // logout user
    const logout = () => {
        setUser(null);
        delete authApi.defaults.headers.common['Authorization'];
    };

    return (
        <AuthContext.Provider
            value={{ user, loading, error, login, register, logout }}
        >
            {children}
        </AuthContext.Provider>
    );
}
