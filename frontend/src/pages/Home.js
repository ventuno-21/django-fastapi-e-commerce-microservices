// Home page: fetch products and show ProductCard list


import React, { useEffect, useState } from 'react';
import { djangoApi } from '../api/apiClient';
import ProductCard from '../components/ProductCard';


export default function Home() {
    const [products, setProducts] = useState([]);
    const [loading, setLoading] = useState(true);


    useEffect(() => {
        const load = async () => {
            try {
                const res = await djangoApi.get('/products/');
                setProducts(res.data);
            } catch (err) {
                console.error('Failed to load products', err);
            } finally {
                setLoading(false);
            }
        };
        load();
    }, []);


    if (loading) return <div>Loading products...</div>;


    return (
        <div style={{ padding: 12 }}>
            <h1>Products</h1>
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(220px, 1fr))', gap: 12 }}>
                {products.map(p => (
                    <ProductCard key={p.id} product={p} />
                ))}
            </div>
        </div>
    );
}