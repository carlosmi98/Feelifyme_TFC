import React from 'react';
import { useDocumentTitle } from '../../../hooks/useDocumentTitle';
import { EditarPerfilContainer } from './components/EditarPerfilContainer/EditarPerfilContainer';

export const EditarPerfil = () => {
    useDocumentTitle('Editar Perfil');
    
    return (
        <EditarPerfilContainer />
    );
};
