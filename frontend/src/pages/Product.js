// src/pages/ProductDetail.js
import React, { useEffect, useState, useContext } from 'react';
import { useParams } from 'react-router-dom';
import { djangoApi } from '../api/apiClient';
import { CartContext } from '../context/CartContext';

export default function ProductDetail() {
    const { id } = useParams();
    const [product, setProduct] = useState(null);
    const [loading, setLoading] = useState(true);
    const { addToCart } = useContext(CartContext);

    useEffect(() => {
        const load = async () => {
            try {
                const res = await djangoApi.get(`/products/${id}/`);
                setProduct(res.data);
            } catch (err) {
                console.error('Failed to load product', err);
            } finally {
                setLoading(false);
            }
        };
        load();
    }, [id]);

    if (loading) return <div>Loading...</div>;
    if (!product) return <div>Product not found</div>;

    return (
        <div style={{ padding: 12 }}>
            <h2>{product.name}</h2>
            <p>{product.description}</p>
            <div>Price: {product.price}</div>
            <button style={{ marginTop: 8 }} onClick={() => addToCart(product.id, 1)}>Add to cart</button>
        </div>
    );
}
