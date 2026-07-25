import React from 'react';
import { getLogroEmoji, formatFecha } from '../../../../../utils/logroUtils';
import './LogroItemCard.css';

export const LogroItemCard = ({ logro }) => {
    const isLocked = !logro.desbloqueado;
    const fecha = logro.fecha_desbloqueo || logro.fecha_obtenido;

    return (
        <div className={`logro-item-card ${isLocked ? 'locked' : 'unlocked'}`}>
            <div className="logro-card-left">
                <span className="logro-card-emoji">{getLogroEmoji(logro)}</span>
                <div className="logro-card-details">
                    <h4>{logro.nombre}</h4>
                    <p>{logro.descripcion}</p>
                    {logro.desbloqueado && fecha && (
                        <span className="fecha-desbloqueo">
                            Obtenido el {formatFecha(fecha)}
                        </span>
                    )}
                </div>
            </div>
            <div className="logro-card-right">
                <div className="logro-puntos-badge">
                    <span className="points-val">+{logro.puntos}</span>
                    <span className="points-lbl">pts</span>
                </div>
            </div>
        </div>
    );
};
