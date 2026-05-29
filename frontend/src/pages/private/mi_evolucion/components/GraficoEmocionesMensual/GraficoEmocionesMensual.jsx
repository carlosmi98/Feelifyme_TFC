import React from 'react';
import ReactECharts from 'echarts-for-react';
import { useEmotionalAssets } from '../../../../../hooks/useEmotionalAssets';
import './GraficoEmocionesMensual.css';

export const GraficoEmocionesMensual = ({ datos }) => {
    const { getEmocionColor } = useEmotionalAssets();

    if (!datos || datos.length === 0) {
        return (
            <div className="grafico-vacio">
                <p>No hay datos suficientes para mostrar el gráfico este mes.</p>
            </div>
        );
    }

    // Preparar datos con colores asignados
    const dataWithColors = datos.map(item => ({
        ...item,
        itemStyle: { color: getEmocionColor(item.name) }
    }));

    const option = {
        tooltip: {
            trigger: 'item',
            formatter: '{b}: {c} ({d}%)' // Muestra: Alegría: 5 (20%)
        },
        legend: {
            bottom: '5%',
            left: 'center',
            textStyle: {
                color: 'var(--text-main)',
                fontFamily: 'nunito-regular'
            }
        },
        series: [
            {
                name: 'Emociones',
                type: 'pie',
                radius: ['40%', '70%'],
                avoidLabelOverlap: false,
                itemStyle: {
                    borderRadius: 10,
                    borderColor: '#fff',
                    borderWidth: 2
                },
                label: {
                    show: false,
                    position: 'center'
                },
                emphasis: {
                    label: {
                        show: true,
                        fontSize: '20',
                        fontWeight: 'bold',
                        fontFamily: 'quicksand-bold'
                    }
                },
                labelLine: {
                    show: false
                },
                data: dataWithColors
            }
        ]
    };

    return (
        <div className="grafico-container">
            <ReactECharts
                option={option}
                style={{ height: '400px', width: '100%' }}
                opts={{ renderer: 'svg' }}
            />
        </div>
    );
};
