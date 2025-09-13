// src/contexts/CartContext.js
// Manages a cart stored in Django session (Redis-backed)
import React, { createContext, useEffect, useState } from 'react';
import { djangoApi } from '../api/apiClient';

export const CartContext = createContext();

export default function CartProvider({ children }) {
    const [cart, setCart] = useState({ items: [], total: 0 });
    const [loading, setLoading] = useState(true);

    const loadCart = async () => {
        try {
            const res = await djangoApi.get('/cart/');
            setCart(res.data);
        } catch (err) {
            console.error('Failed to load cart', err);
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        loadCart();
    }, []);

    const addToCart = async (productId, qty = 1) => {
        try {
            await djangoApi.post('/cart/add/', { product_id: productId, qty });
            await loadCart();
        } catch (err) {
            throw err;
        }
    };

    const updateCart = async (productId, qty) => {
        try {
            await djangoApi.post('/cart/update/', { product_id: productId, qty });
            await loadCart();
        } catch (err) {
            throw err;
        }
    };

    const removeFromCart = async (productId) => {
        try {
            await djangoApi.post('/cart/remove/', { product_id: productId });
            await loadCart();
        } catch (err) {
            throw err;
        }
    };

    const clearCart = async () => {
        try {
            await djangoApi.post('/cart/clear/');
            await loadCart();
        } catch (err) {
            throw err;
        }
    };

    return (
        <CartContext.Provider value={{ cart, loading, addToCart, updateCart, removeFromCart, clearCart }}>
            {children}
        </CartContext.Provider>
    );
}
