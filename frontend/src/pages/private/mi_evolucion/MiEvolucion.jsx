import React from 'react';
import { useDocumentTitle } from '../../../hooks/useDocumentTitle';
import { MiEvolucionContainer } from './components/MiEvolucionContainer/MiEvolucionContainer';

export const MiEvolucion = () => {
    useDocumentTitle('Mi Evolución');
    
    return (
        <MiEvolucionContainer />
    );
};
