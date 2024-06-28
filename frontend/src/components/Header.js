import React from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

function Header() {
    const { isAuthenticated, logout } = useAuth();

    return (
        <header>
            <nav>
                <ul>
                    {isAuthenticated ? (
                        <>
                            <li><Link to="/">Dashboard</Link></li>
                            <li><Link to="/bots">Bots</Link></li>
                            <li><Link to="/rag">RAG Interface</Link></li>
                            <li><Link to="/settings">Settings</Link></li>
                            <li><button onClick={logout}>Logout</button></li>
                        </>
                    ) : (
                        <>
                            <li><Link to="/login">Login</Link></li>
                            <li><Link to="/register">Register</Link></li>
                        </>
                    )}
                </ul>
            </nav>
        </header>
    );
}

export default Header;