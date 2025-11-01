import React, { createContext, useState, useEffect } from 'react';

const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
    const [isAuthenticated, setIsAuthenticated] = useState(false);
    const [user, setUser] = useState(null);

    useEffect(() => {
        const token = localStorage.getItem('access-token');
        if (token) {
            setIsAuthenticated(true);
        }
    }, []);

    const login = (tokens) => {
        localStorage.setItem('access-token', tokens.access);
        localStorage.setItem('refresh-token', tokens.refresh);
        setIsAuthenticated(true);
    };
    const logout = () => {
        localStorage.removeItem('access-token');
        localStorage.removeItem('refresh-token');
        setIsAuthenticated(false);
        setUser(null);
    };

    return (
        <AuthContext.Provider value={{ isAuthenticated, user, login, logout }}>
            {children}
        </AuthContext.Provider>
    );
};

export default AuthContext;
