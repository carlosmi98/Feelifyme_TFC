import { useState, useEffect } from 'react';
import { getEvolucionMensual } from '../services/diaryService';

export const useEvolucion = (mes) => {
    const [datos, setDatos] = useState({ emociones: [], actividades: [] });
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);

    useEffect(() => {
        if (!mes) return;

        const fetchData = async () => {
            try {
                setLoading(true);
                const result = await getEvolucionMensual(mes);
                setDatos(result);
                setError(null);
            } catch (err) {
                console.error("Error al cargar evolución mensual:", err);
                setError(err);
                setDatos({ emociones: [], actividades: [] });
            } finally {
                setLoading(false);
            }
        };

        fetchData();
    }, [mes]);

    return { datos, loading, error };
};
