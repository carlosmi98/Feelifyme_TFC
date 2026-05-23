import React from 'react';
import { useNavigate } from 'react-router-dom';
import { SectionCard } from '../../../../../componentes/generales';
import './AvatarCard.css';

export const AvatarCard = ({ userProfile }) => {
    const navigate = useNavigate();

    return (
        <SectionCard className="text-center">
            <img 
                src="https://ui-avatars.com/api/?name=User&background=random" 
                alt="Avatar" 
                className="avatar-img" 
            />
            <h2>{userProfile?.profile?.nombre} {userProfile?.profile?.apellido1}</h2>
            <p>{userProfile?.email}</p>
            
            <button 
                className="btn-editar-avatar"
                onClick={() => navigate('/perfil/editar', { state: { userProfile } })}
            >
                Editar perfil
            </button>
        </SectionCard>
    );
};
