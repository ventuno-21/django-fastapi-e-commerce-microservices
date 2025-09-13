// src/pages/OrdersPage.js
import React, { useEffect, useState } from 'react';
import { djangoApi } from '../api/apiClient';

export default function OrdersPage() {
    const [orders, setOrders] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const load = async () => {
            try {
                const res = await djangoApi.get('/orders/');
                setOrders(res.data);
            } catch (err) {
                console.error('Failed to load orders', err);
            } finally {
                setLoading(false);
            }
        };
        load();
    }, []);

    if (loading) return <div>Loading orders...</div>;
    if (!orders.length) return <div>No orders yet.</div>;

    return (
        <div>
            <h2>Your Orders</h2>
            {orders.map(order => (
                <div key={order.id} style={{ border: '1px solid #ddd', padding: 8, marginBottom: 8 }}>
                    <div><strong>Order #{order.id}</strong></div>
                    <div>Date: {order.created_at}</div>
                    <div>Total: {order.total}</div>
                    <div>Items:</div>
                    <ul>
                        {order.items.map(i => <li key={i.product_id}>{i.name} x {i.qty}</li>)}
                    </ul>
                </div>
            ))}
        </div>
    );
}
