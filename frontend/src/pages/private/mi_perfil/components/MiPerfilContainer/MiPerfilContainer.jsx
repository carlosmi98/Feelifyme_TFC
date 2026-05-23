import React from 'react';
import { useAuth } from '../../../../../context/AuthContext';
import { deleteAccount } from '../../../../../services/authService';
import { useProfile } from '../../../../../hooks/useProfile';
import { Spinner } from '../../../../../componentes/generales';
import { Title } from '../../../../../componentes/generales';
import { AvatarCard } from '../AvatarCard/AvatarCard';
import { DangerZone } from '../DangerZone/DangerZone';
import { InfoPersonal } from '../InfoPersonal/InfoPersonal';
import { Preferencias } from '../Preferencias/Preferencias';
import './MiPerfilContainer.css';

export const MiPerfilContainer = () => {
    const { logout } = useAuth();

    const { userProfile, loading } = useProfile();

    const handleDeleteAccount = async () => {
        const confirmacion = window.confirm("¿Estás seguro? Esta acción eliminará permanentemente tu cuenta y todos tus registros. No se puede deshacer.");
        if (confirmacion) {
            try {
                await deleteAccount();
                alert("Cuenta eliminada correctamente.");
                logout();
            } catch (error) {
                alert("Error al eliminar la cuenta.");
                console.error(error);
            }
        }
    };

    if (loading) return <Spinner />;

    return (
        <div className="layout-page">
            <Title nivel={1} className="titulo-principal text-center">Mi Perfil</Title>

            <div className="mi-perfil-container">
                <div className="perfil-col-izq">
                    <AvatarCard userProfile={userProfile} />
                    <DangerZone onDeleteAccount={handleDeleteAccount} />
                </div>

                <div className="perfil-col-der">
                    <InfoPersonal userProfile={userProfile} />
                    <Preferencias />
                </div>
            </div>
        </div>
    );
};
