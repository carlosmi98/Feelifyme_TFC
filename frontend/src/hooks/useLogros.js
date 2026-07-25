import { useState, useEffect } from 'react';
import { getMisLogros } from '../services/diaryService';

export const useLogros = () => {
    const [datos, setDatos] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        const fetchLogros = async () => {
            try {
                setLoading(true);
                const res = await getMisLogros();
                setDatos(res);
                setError(null);
            } catch (err) {
                console.error("Error al cargar logros:", err);
                setError(err);
            } finally {
                setLoading(false);
            }
        };

        fetchLogros();
    }, []);

    return { datos, loading, error };
};
