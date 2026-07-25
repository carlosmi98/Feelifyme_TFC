/**
 * Mapeador de emojis para representar medallas e hitos de manera premium y consistente.
 */
export const getLogroEmoji = (logro) => {
    if (!logro) return '🏆';
    if (logro.es_secreto && !logro.desbloqueado) return '🔒';
    
    const nombre = logro.nombre || '';
    const nombreLower = nombre.toLowerCase();
    
    // Prioridad 1: Coincidencia por palabras clave en el nombre del logro
    if (nombreLower.includes('racha')) return '🔥';
    if (nombreLower.includes('primer paso') || nombreLower.includes('comienzo')) return '⭐';
    if (nombreLower.includes('explorador')) return '🧭';
    if (nombreLower.includes('arcoíris') || nombreLower.includes('arcoiris')) return '🌈';
    if (nombreLower.includes('reflexión') || nombreLower.includes('reflexivo')) return '✍️';
    if (nombreLower.includes('actividad')) return '🏃';
    if (nombreLower.includes('recomendación') || nombreLower.includes('recomendacion')) return '💡';
    if (nombreLower.includes('bienestar')) return '☀️';
    if (nombreLower.includes('estabilidad')) return '🏔️';
    if (nombreLower.includes('autocuidado')) return '🧘';
    if (nombreLower.includes('medianoche')) return '🌑';
    if (nombreLower.includes('amanecer')) return '🌅';
    if (nombreLower.includes('regreso')) return '🔄';
    if (nombreLower.includes('cumpleaños')) return '🎂';
    if (nombreLower.includes('festivo')) return '🎉';

    // Prioridad 2: Fallback por categoría
    const categoria = logro.categoria || '';
    const catLower = categoria.toLowerCase();
    if (catLower === 'rachas') return '🔥';
    if (catLower === 'emociones') return '🌈';
    if (catLower === 'reflexiones') return '📝';
    if (catLower === 'actividades') return '🏃';

    // Prioridad 3: Fallback por tipo
    const tipo = logro.tipo || '';
    const tipoLower = tipo.toLowerCase();
    if (tipoLower === 'secreto') return '🔮';
    if (tipoLower === 'hito') return '🏆';

    return '🏅';
};

/**
 * Formatea una fecha ISO a formato de legibilidad en español (dd/mm/aaaa)
 */
export const formatFecha = (fechaStr) => {
    if (!fechaStr) return '';
    try {
        const d = new Date(fechaStr);
        if (isNaN(d.getTime())) return '';
        return d.toLocaleDateString('es-ES', { day: '2-digit', month: '2-digit', year: 'numeric' });
    } catch {
        return '';
    }
};
