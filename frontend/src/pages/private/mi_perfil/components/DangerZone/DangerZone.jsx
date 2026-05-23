import React from 'react';
import { SectionCard } from '../../../../../componentes/generales';
import './DangerZone.css';

export const DangerZone = ({ onDeleteAccount }) => {
    return (
        <SectionCard titulo="Danger zone" className="danger-zone-card">
            <button onClick={onDeleteAccount} className="btn-peligro">Eliminar cuenta</button>
            <button onClick={() => alert("Función disponible próximamente")} className="btn-link">Descargar mis datos</button>
            <button onClick={() => alert("Función disponible próximamente")} className="btn-link">Resetear estadísticas</button>
        </SectionCard>
    );
};
