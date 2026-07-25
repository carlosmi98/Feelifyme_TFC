import React from 'react';
import { useDocumentTitle } from '../../../hooks/useDocumentTitle';
import { LogrosContainer } from './components/LogrosContainer/LogrosContainer';

export const LogrosPage = () => {
    useDocumentTitle('Mis Logros');

    return (
        <LogrosContainer />
    );
};
