// Simple navbar showing auth links and cart count


import React, { useContext } from 'react';
import { Link } from 'react-router-dom';
import { CartContext } from '../context/CartContext';
import { AuthContext } from '../context/AuthContext';


export default function Navbar() {
    const { cart } = useContext(CartContext);
    const { user, logout } = useContext(AuthContext);


    // compute total quantity
    const count = cart.items?.reduce((sum, it) => sum + (it.qty || 0), 0) || 0;


    return (
        <nav style={{ padding: '12px', borderBottom: '1px solid #ccc' }}>
            <Link to="/">Home</Link>
            {' | '}
            <Link to="/cart">Cart ({count})</Link>
            {' | '}
            {user ? (
                <>
                    <span style={{ marginLeft: 8 }}>Hello, {user.username}</span>
                    <button style={{ marginLeft: 12 }} onClick={logout}>Logout</button>
                </>
            ) : (
                <>
                    <Link to="/auth/login">Login</Link>
                    {' | '}
                    <Link to="/auth/register">Register</Link>
                </>
            )}
        </nav>
    );
}