import { useState, useEffect } from 'react';
import { getMyProfile } from '../services/authService';
import { useAuth } from '../context/AuthContext';

export const useProfile = () => {
    const { logout } = useAuth();
    const [userProfile, setUserProfile] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        const fetchProfile = async () => {
            try {
                setLoading(true);
                const data = await getMyProfile();
                setUserProfile(data);
                setError(null);
            } catch (err) {
                console.error("Error cargando el perfil", err);
                setError(err);
                if (err.response?.status === 401) {
                    logout();
                }
            } finally {
                setLoading(false);
            }
        };

        fetchProfile();
    }, [logout]);

    return { userProfile, loading, error };
};
