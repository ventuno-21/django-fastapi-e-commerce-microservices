// src/pages/ProfilePage.js
import React, { useContext, useState, useEffect } from 'react';
import { AuthContext } from '../context/AuthContext';
import { authApi } from '../api/apiClient';

export default function ProfilePage() {
    const { user, loading } = useContext(AuthContext);
    const [form, setForm] = useState({ username: '', email: '' });
    const [saving, setSaving] = useState(false);
    const [message, setMessage] = useState(null);

    useEffect(() => {
        if (user) setForm({ username: user.username || '', email: user.email || '' });
    }, [user]);

    const handleChange = (e) => setForm({ ...form, [e.target.name]: e.target.value });

    const handleSave = async () => {
        setSaving(true);
        setMessage(null);
        try {
            await authApi.put('/auth/profile/', form);
            setMessage('Saved.');
        } catch (err) {
            setMessage('Save failed.');
        } finally {
            setSaving(false);
        }
    };

    if (loading) return <div>Loading...</div>;
    if (!user) return <div>Please login to view profile.</div>;

    return (
        <div>
            <h2>Profile</h2>
            {message && <div>{message}</div>}
            <div>
                <label>Username</label><br />
                <input name="username" value={form.username} onChange={handleChange} />
            </div>
            <div>
                <label>Email</label><br />
                <input name="email" value={form.email} onChange={handleChange} />
            </div>
            <button onClick={handleSave} disabled={saving}>{saving ? 'Saving...' : 'Save'}</button>
        </div>
    );
}
