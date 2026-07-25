import React, { useEffect, useState } from 'react';
import { getLogroEmoji } from '../../../utils/logroUtils';
import './ModalLogroDesbloqueado.css';

export const ModalLogroDesbloqueado = ({ logros = [], onClose }) => {
    const [indiceActual, setIndiceActual] = useState(0);
    const [mostrar, setMostrar] = useState(false);

    useEffect(() => {
        if (logros.length > 0) {
            setMostrar(true);
        }
    }, [logros]);

    if (logros.length === 0 || !mostrar) return null;

    const logroActual = logros[indiceActual];

    const siguienteLogro = () => {
        if (indiceActual < logros.length - 1) {
            // Animar transición al siguiente
            setIndiceActual(prev => prev + 1);
        } else {
            setMostrar(false);
            if (onClose) onClose();
        }
    };

    return (
        <div className="logro-modal-overlay">
            {/* Partículas de confeti simuladas en CSS */}
            <div className="confetti-container">
                <div className="confetti red"></div>
                <div className="confetti yellow"></div>
                <div className="confetti blue"></div>
                <div className="confetti green"></div>
                <div className="confetti purple"></div>
                <div className="confetti orange"></div>
            </div>

            <div className="logro-modal-card">
                <div className="badge-glow"></div>
                
                <div className="logro-modal-header">
                    <span className="logro-header-tag">NUEVO LOGRO</span>
                    <h2>¡Desbloqueado!</h2>
                </div>

                <div className="logro-modal-body">
                    <div className="logro-avatar-wrapper">
                        <span className="logro-modal-emoji" role="img" aria-label="logro">
                            {getLogroEmoji(logroActual)}
                        </span>
                    </div>

                    <h3 className="logro-modal-titulo">{logroActual.nombre}</h3>
                    <p className="logro-modal-descripcion">{logroActual.descripcion}</p>
                    
                    <div className="logro-modal-points">
                        <span className="points-number">+{logroActual.puntos}</span>
                        <span className="points-label">puntos</span>
                    </div>
                </div>

                <div className="logro-modal-footer">
                    <button className="btn-logro-siguiente" onClick={siguienteLogro}>
                        {indiceActual < logros.length - 1 ? 'Siguiente Logro' : '¡Genial!'}
                    </button>
                </div>
            </div>
        </div>
    );
};
