// src/components/ProductCard.js
import React from 'react';
import { Link } from 'react-router-dom';

export default function ProductCard({ product }) {
    return (
        <div style={{ border: '1px solid #ddd', padding: 12, borderRadius: 6 }}>
            <h3>{product.name}</h3>
            <p>{product.description}</p>
            <div>Price: {product.price}</div>
            <div style={{ marginTop: 8 }}>
                <Link to={`/product/${product.id}`}>View</Link>
            </div>
        </div>
    );
}
