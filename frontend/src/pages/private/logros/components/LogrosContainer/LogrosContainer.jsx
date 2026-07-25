import React from 'react';
import { Title, Spinner, SectionCard } from '../../../../../componentes/generales';
import { useLogros } from '../../../../../hooks/useLogros';
import { LogroItemCard } from '../LogroItemCard/LogroItemCard';
import './LogrosContainer.css';

export const LogrosContainer = () => {
    const { datos, loading, error } = useLogros();

    if (loading) return <Spinner />;

    if (error || !datos) {
        return (
            <div className="layout-page logros-error-page">
                <Title nivel={1} className="titulo-principal text-center">Logros personales</Title>
                <div className="error-card">
                    <p>Ha ocurrido un error al cargar tus logros. Por favor, inténtalo más tarde.</p>
                </div>
            </div>
        );
    }

    const {
        desbloqueados = [],
        no_desbloqueados = [],
        puntos_totales = 0,
        racha_actual = 0,
        reflexiones_count = 0,
        recomendaciones_count = 0
    } = datos;

    // Combinar desbloqueados y bloqueados
    const todosLosLogros = [
        ...desbloqueados.map(l => ({ ...l, desbloqueado: true })),
        ...no_desbloqueados.map(l => ({ ...l, desbloqueado: false }))
    ].sort((a, b) => a.id - b.id);

    // Filtrar por secciones
    const medallasYStreaks = todosLosLogros.filter(l => 
        (l.tipo === 'medalla' || l.tipo === 'racha') && !l.es_secreto
    );
    const hitosImportantes = todosLosLogros.filter(l => 
        (l.tipo === 'hito' || l.tipo === 'especial') && !l.es_secreto
    );
    const logrosSecretos = todosLosLogros.filter(l => 
        l.es_secreto || l.tipo === 'secreto'
    );

    return (
        <div className="layout-page logros-page-wrapper">
            <div className="logros-header-info">
                <Title nivel={1} className="titulo-principal text-center">Logros personales</Title>
                <div className="puntos-totales-badge">
                    <span className="pts-totales-num">{puntos_totales}</span>
                    <span className="pts-totales-lbl">Puntos Totales</span>
                </div>
            </div>

            {/* Fila Superior: 3 Tarjetas de Estadísticas */}
            <div className="logros-stats-grid">
                <div className="logros-stat-card">
                    <span className="stat-card-icon">🔥</span>
                    <div className="stat-card-info">
                        <h3>Días seguidos registrando</h3>
                        <span className="stat-number">{racha_actual}</span>
                    </div>
                </div>

                <div className="logros-stat-card">
                    <span className="stat-card-icon">📝</span>
                    <div className="stat-card-info">
                        <h3>Reflexiones escritas</h3>
                        <span className="stat-number">{reflexiones_count}</span>
                    </div>
                </div>

                <div className="logros-stat-card">
                    <span className="stat-card-icon">💡</span>
                    <div className="stat-card-info">
                        <h3>Recomendaciones</h3>
                        <span className="stat-number">{recomendaciones_count}</span>
                    </div>
                </div>
            </div>

            {/* Secciones de Logros */}
            <div className="logros-sections-container">
                <SectionCard titulo="Medallas de Logro" className="logros-section-box">
                    <div className="logros-list-grid">
                        {medallasYStreaks.map(logro => (
                            <LogroItemCard key={logro.id} logro={logro} />
                        ))}
                    </div>
                </SectionCard>

                <SectionCard titulo="Hitos Importantes" className="logros-section-box">
                    <div className="logros-list-grid">
                        {hitosImportantes.map(logro => (
                            <LogroItemCard key={logro.id} logro={logro} />
                        ))}
                    </div>
                </SectionCard>

                {logrosSecretos.length > 0 && (
                    <SectionCard titulo="Logros Secretos 🔮" className="logros-section-box logros-secretos-box">
                        <div className="logros-list-grid">
                            {logrosSecretos.map(logro => (
                                <LogroItemCard key={logro.id} logro={logro} />
                            ))}
                        </div>
                    </SectionCard>
                )}
            </div>
        </div>
    );
};
