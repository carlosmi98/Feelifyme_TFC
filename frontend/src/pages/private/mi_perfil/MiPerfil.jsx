import React from 'react';
import { useDocumentTitle } from '../../../hooks/useDocumentTitle';
import { MiPerfilContainer } from './components/MiPerfilContainer/MiPerfilContainer';

export const MiPerfil = () => {
    useDocumentTitle('Mi Perfil');
    
    return (
        <MiPerfilContainer />
    );
};
