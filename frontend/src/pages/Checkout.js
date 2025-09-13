// src/pages/CheckoutPage.js
import React, { useState } from 'react';
import { djangoApi } from '../api/apiClient';
import { useNavigate } from 'react-router-dom';

export default function CheckoutPage() {
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);
    const [success, setSuccess] = useState(null);
    const nav = useNavigate();

    const doCheckout = async () => {
        setLoading(true);
        setError(null);
        try {
            const res = await djangoApi.post('/api/checkout/');
            // assume backend returns { order_id: .. }
            setSuccess(res.data);
            // navigate to orders or confirmation
            nav('/orders');
        } catch (err) {
            setError('Checkout failed');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div>
            <h2>Checkout (Fake)</h2>
            <p>This is a fake checkout. Clicking confirm will convert cart to an order on the server.</p>
            {error && <div style={{ color: 'red' }}>{error}</div>}
            <button onClick={doCheckout} disabled={loading}>{loading ? 'Processing...' : 'Confirm & Pay'}</button>
            {success && <div>Success: {JSON.stringify(success)}</div>}
        </div>
    );
}
