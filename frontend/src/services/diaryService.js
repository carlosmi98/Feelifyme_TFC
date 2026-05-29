import api from '../api/axiosInstance';

/**
 * Obtiene el árbol completo de emociones (jerarquía) para la rueda.
 */
export const getEmocionesArbol = async () => {
    const response = await api.get('emociones/arbol/');
    return response.data;
};

/**
 * Obtiene el catálogo completo de actividades desde el backend.
 */
export const getActividades = async () => {
    const response = await api.get('actividades/')
    return response.data;
}

/**
 * Obtiene el resumen emocional de un mes específico para el calendario.
 * @param {string} mes - Formato "YYYY-MM"
 */
export const getCalendarioResumen = async (mes) => {
    const response = await api.get(`calendario/resumen/?mes=${mes}`)
    return response.data
}

/**
 * Obtiene el detalle cronológico de un día específico.
 * @param {string} fecha - Formato "YYYY-MM-DD"
 */
export const getResumenDiario = async (fecha) => {
    const response = await api.get(`resumen-dia/?fecha=${fecha}`)
    return response.data;
};

/**
 * Guarda un registro diario de emociones y actividades.
 * @param {Object} payload - Datos del registro (emociones, actividades, nota, fecha).
 */
export const postRegistroDiario = async (payload) => {
    const response = await api.post('registro-diario/', payload)
    return response.data;
}

/**
 * Obtiene el resumen de evolución emocional (conteos) de un mes específico.
 * @param {string} mes - Formato "YYYY-MM"
 */
export const getEvolucionMensual = async (mes) => {
    const response = await api.get(`evolucion/mensual/?mes=${mes}`);
    return response.data;
};