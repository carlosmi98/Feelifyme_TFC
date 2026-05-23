import React, { useState, useEffect } from 'react';
import ReactECharts from 'echarts-for-react';
import './RuedaEmociones.css';
import { Title } from "../../../../../componentes/generales";
import { useEmocionesArbol } from "../../../../../hooks/useEmocionesArbol";

export const RuedaEmociones = ({ seleccionadasActuales, onSelectEmociones }) => {
    const { arbol, loading, error } = useEmocionesArbol();
    const [windowWidth, setWindowWidth] = useState(window.innerWidth);

    const handleClick = (params) => {
        const emocionId = params.data?.id;
        if (!emocionId) return; // Clic en el centro para volver atrás

        // Si estamos en móvil (donde funciona rootToNode) y la emoción TIENE hijas (no es isLeaf),
        // evitamos seleccionarla para que React no recargue el componente y corte la animación de zoom de ECharts.
        if (windowWidth < 768 && !params.data?.isLeaf) {
            return; 
        }

        const updated = seleccionadasActuales.includes(emocionId)
            ? seleccionadasActuales.filter(e => e !== emocionId)
            : [...seleccionadasActuales, emocionId];
        
        onSelectEmociones(updated);
    };

    const getBaseColor = (name) => {
        const lower = name.toLowerCase();
        if (lower === 'ira') return '#f43f5e';
        if (lower === 'miedo') return '#d946ef';
        if (lower === 'disgusto') return '#f97316';
        if (lower === 'tristeza') return '#10b981';
        if (lower === 'felicidad') return '#eab308';
        if (lower === 'sorpresa') return '#0ea5e9';
        return null;
    };

    const formatDataForEcharts = (nodes, parentColor = null, seleccionadasList = []) => {
        return nodes.map(node => {
            let nombreLimpio = node.name;
            if (nombreLimpio.includes('(')) {
                nombreLimpio = nombreLimpio.split('(')[0].trim();
            }

            const color = getBaseColor(node.name) || parentColor;
            const isSelected = seleccionadasList.includes(node.id);
            const hasSelection = seleccionadasList.length > 0;

            const opacity = hasSelection ? (isSelected ? 0.35 : 1) : 1;
            const borderColor = isSelected ? '#000000' : 'white';
            const borderWidth = isSelected ? 3 : 1.5;

            const newNode = {
                id: node.id,
                name: nombreLimpio,
                value: node.loc || 1,
                isLeaf: !node.children || node.children.length === 0,
                itemStyle: {
                    color: color,
                    opacity: opacity,
                    borderColor: borderColor,
                    borderWidth: borderWidth
                }
            };

            if (node.children && node.children.length > 0) {
                newNode.children = formatDataForEcharts(node.children, color, seleccionadasList);
                delete newNode.value;
            }

            return newNode;
        });
    };

    useEffect(() => {
        const handleResize = () => setWindowWidth(window.innerWidth);
        window.addEventListener('resize', handleResize);
        return () => window.removeEventListener('resize', handleResize);
    }, []);

    const getFontSizes = () => {
        if (windowWidth < 480) return { level1: 10, level2: 8.5, level3: 7 };
        if (windowWidth < 768) return { level1: 11, level2: 9.5, level3: 8 };
        return { level1: 13, level2: 11, level3: 8.5 };
    };

    const fonts = getFontSizes();

    if (loading) return <div className="rueda-container">Cargando emociones...</div>;
    if (error) return <div className="rueda-container">No se pudo cargar la rueda de emociones.</div>;

    const echartsData = arbol?.children ? formatDataForEcharts(arbol.children, null, seleccionadasActuales) : null;

    const option = {
        tooltip: { trigger: 'item', formatter: '{b}' },
        series: {
            type: 'sunburst',
            data: echartsData,
            radius: [0, '95%'],
            sort: null,
            nodeClick: windowWidth < 768 ? 'rootToNode' : false,
            emphasis: { focus: 'ancestor' },
            itemStyle: { borderRadius: 2 },
            label: {
                rotate: 'radial',
                color: '#ffffff',
                fontWeight: 'bold',
                minAngle: 0,
                textBorderColor: 'rgba(0,0,0,0)',
                fontFamily: 'emociones-font, sans-serif'
            },
            levels: [
                {},
                { label: { rotate: 'radial', fontSize: fonts.level1, color: '#fff', align: 'center' } },
                { label: { align: 'center', fontSize: fonts.level2, minAngle: 0 } },
                { label: { align: 'center', fontSize: fonts.level3, minAngle: 0 } }
            ]
        }
    };

    return (
        <section className="rueda-seccion-container">
            <Title className="rueda-titulo">¿Cómo te sientes hoy?</Title>
            <p className="rueda-descripcion">Selecciona una emoción de la rueda para tu registro diario.</p>
            <p className="rueda-tip">
                💡 Tip: Toca cualquier emoción para hacer zoom y verla en detalle. Pulsa en el centro para volver atrás.
            </p>
            <div className="rueda-container">
                <ReactECharts
                    option={option}
                    style={{ height: '100%', width: '100%' }}
                    opts={{ renderer: 'svg' }}
                    onEvents={{ click: handleClick }}
                />
            </div>
        </section>
    );
};
