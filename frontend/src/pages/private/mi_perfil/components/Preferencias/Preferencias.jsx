import React from 'react';
import { SectionCard } from '../../../../../componentes/generales';
import './Preferencias.css';

export const Preferencias = () => {
    return (
        <SectionCard titulo="Preferencias">
            <div className="info-display">
                <p><strong>Tema:</strong> auto</p>
                <p><strong>Idioma:</strong> ES</p>
                <button 
                    className="btn-editar-seccion"
                    onClick={() => alert("Gestión de preferencias disponible próximamente")}
                >
                    Editar preferencias
                </button>
            </div>
        </SectionCard>
    );
};
