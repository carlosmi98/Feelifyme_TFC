import React from 'react';
import { useNavigate } from 'react-router-dom';
import { SectionCard } from '../../../../../componentes/generales';
import './InfoPersonal.css';

export const InfoPersonal = ({ userProfile }) => {
    const navigate = useNavigate();

    return (
        <SectionCard titulo="Información personal">
            <div className="info-display">
                <p><strong>Nombre:</strong> {userProfile?.profile?.nombre || '-'}</p>
                <p><strong>Primer Apellido:</strong> {userProfile?.profile?.apellido1 || '-'}</p>
                <p><strong>Segundo Apellido:</strong> {userProfile?.profile?.apellido2 || '-'}</p>
                <p><strong>Email:</strong> {userProfile?.email}</p>
                
                <button 
                    className="btn-editar-seccion"
                    onClick={() => navigate('/perfil/editar', { state: { userProfile } })}
                >
                    Editar perfil
                </button>
            </div>
        </SectionCard>
    );
};
