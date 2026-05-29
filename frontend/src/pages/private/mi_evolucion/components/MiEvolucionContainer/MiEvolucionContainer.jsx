import React, { useState } from 'react';
import { Title, Spinner } from '../../../../../componentes/generales';
import { useEvolucion } from '../../../../../hooks/useEvolucion';
import { GraficoEmocionesMensual } from '../GraficoEmocionesMensual/GraficoEmocionesMensual';
import { GraficoActividadesMensual } from '../GraficoActividadesMensual/GraficoActividadesMensual';
import { format, parseISO } from 'date-fns';
import { es } from 'date-fns/locale';
import './MiEvolucionContainer.css';

export const MiEvolucionContainer = () => {
    // Por defecto el mes actual en formato YYYY-MM
    const [mesSeleccionado, setMesSeleccionado] = useState(
        new Date().toISOString().slice(0, 7)
    );

    const { datos, loading, error } = useEvolucion(mesSeleccionado);

    // Formatear mes para mostrarlo bonito ("mayo de 2026")
    const getMesNombre = (mesStr) => {
        try {
            const date = parseISO(`${mesStr}-01`);
            const txt = format(date, "MMMM 'de' yyyy", { locale: es });
            return txt.charAt(0).toUpperCase() + txt.slice(1);
        } catch (e) {
            return mesStr;
        }
    };

    return (
        <div className="layout-page">
            <Title nivel={1} className="titulo-principal text-center">Mi Evolución</Title>
            
            <div className="evolucion-container">
                <header className="evolucion-header">
                    <h2>Resumen de {getMesNombre(mesSeleccionado)}</h2>
                    <div className="selector-mes">
                        <label htmlFor="mes-selector">Cambiar mes:</label>
                        <input 
                            type="month" 
                            id="mes-selector" 
                            value={mesSeleccionado}
                            onChange={(e) => setMesSeleccionado(e.target.value)}
                        />
                    </div>
                </header>

                <main className="evolucion-contenido">
                    {loading ? (
                        <Spinner />
                    ) : error ? (
                        <p className="error-msg">Ha ocurrido un error al cargar los datos.</p>
                    ) : (
                        <div className="graficos-grid">
                            <div className="grafico-wrapper">
                                <h3 className="grafico-titulo">Proporción de Emociones</h3>
                                <GraficoEmocionesMensual datos={datos.emociones} />
                            </div>
                            <div className="grafico-wrapper">
                                <h3 className="grafico-titulo">Actividades Frecuentes</h3>
                                <GraficoActividadesMensual datos={datos.actividades} />
                            </div>
                        </div>
                    )}
                </main>
            </div>
        </div>
    );
};
