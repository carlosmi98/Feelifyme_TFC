import React from 'react';
import ReactECharts from 'echarts-for-react';

export const GraficoActividadesMensual = ({ datos }) => {
    if (!datos || datos.length === 0) {
        return (
            <div className="grafico-vacio">
                <p>No hay actividades registradas este mes.</p>
            </div>
        );
    }

    const formatLabel = (name) => {
        const conSaltos = name.replace(/_/g, '\n');
        return conSaltos.charAt(0).toUpperCase() + conSaltos.slice(1);
    };

    // Eje Y = Categorías (nombres), Eje X = Valores numéricos.
    const labels = datos.map(item => formatLabel(item.name));
    const values = datos.map(item => item.value);

    const option = {
        tooltip: {
            trigger: 'axis',
            axisPointer: {
                type: 'shadow'
            }
        },
        grid: {
            left: '3%',
            right: '4%',
            bottom: '3%',
            containLabel: true
        },
        xAxis: {
            type: 'value',
            boundaryGap: [0, 0.01],
            axisLabel: {
                color: 'var(--text-soft)',
                fontFamily: 'nunito-regular'
            }
        },
        yAxis: {
            type: 'category',
            data: labels,
            axisLabel: {
                color: 'var(--text-main)',
                fontFamily: 'nunito-bold',
                fontSize: 14
            }
        },
        series: [
            {
                name: 'Frecuencia',
                type: 'bar',
                data: values,
                itemStyle: {
                    color: 'var(--color-secondary)',
                    borderRadius: [0, 5, 5, 0]
                },
                emphasis: {
                    itemStyle: {
                        color: 'var(--color-primary)'
                    }
                },
                label: {
                    show: true,
                    position: 'right',
                    color: 'var(--text-main)',
                    fontFamily: 'nunito-bold'
                }
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
