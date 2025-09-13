// src/pages/CartPage.js
import React, { useContext } from 'react';
import { CartContext } from '../context/CartContext';
import { Link, useNavigate } from 'react-router-dom';

export default function CartPage() {
    const { cart, loading, updateCart, removeFromCart, clearCart } = useContext(CartContext);
    const nav = useNavigate();

    if (loading) return <div>Loading cart...</div>;
    if (!cart.items?.length) return <div>Cart is empty. <Link to='/'>Shop now</Link></div>;

    return (
        <div>
            <h2>Your Cart</h2>
            {cart.items.map(item => (
                <div key={item.product_id} style={{ borderBottom: '1px solid #eee', padding: 8 }}>
                    <div><strong>{item.name}</strong></div>
                    <div>Price: {item.price}</div>
                    <div>Qty: {item.qty}</div>
                    <button onClick={() => updateCart(item.product_id, item.qty + 1)}>+</button>
                    <button onClick={() => updateCart(item.product_id, Math.max(1, item.qty - 1))}>-</button>
                    <button onClick={() => removeFromCart(item.product_id)}>Remove</button>
                </div>
            ))}
            <h3>Total: {cart.total}</h3>
            <button onClick={() => nav('/checkout')}>Proceed to Checkout</button>
            <button onClick={() => clearCart()} style={{ marginLeft: 8 }}>Clear Cart</button>
        </div>
    );
}
