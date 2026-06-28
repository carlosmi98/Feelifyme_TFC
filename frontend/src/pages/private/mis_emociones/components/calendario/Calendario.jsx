import { useState } from "react";
import {
    startOfMonth,
    endOfMonth,
    startOfWeek,
    endOfWeek,
    eachDayOfInterval,
    addMonths,
    subMonths,
    format,
    isSameMonth,
    isToday,
    isAfter
} from "date-fns";
import { es } from "date-fns/locale";
import { CasillaDia } from "./CasillaDia";
import { useCalendario } from "../../../../../hooks/useCalendario";
import { ButtonGroup, Button } from "../../../../../componentes/generales";
import "./Calendario.css";

export const Calendario = () => {

    const [mesActual, setMesActual] = useState(new Date())
    const { datosCalendario, loading } = useCalendario(mesActual);

    const inicioMes = startOfMonth(mesActual)
    const finMes = endOfMonth(mesActual)
    const inicioCuadricula = startOfWeek(inicioMes, { weekStartsOn: 1 })
    const finCuadricula = endOfWeek(finMes, { weekStartsOn: 1 })

    const dias = eachDayOfInterval({
        start: inicioCuadricula,
        end: finCuadricula
    })

    return (
        <section className="calendario-container">
            <header className="calendario-header">
                <button className="izquierda" onClick={() => setMesActual(subMonths(mesActual, 1))}>
                    ←
                </button>

                <h2>{format(mesActual, "MMMM yyyy", { locale: es })}</h2>

                <button className="derecha" onClick={() => setMesActual(addMonths(mesActual, 1))}>
                    →
                </button>
            </header>

            {loading && <div className="cargando-overlay">Cargando...</div>}

            <ul className="grid-calendario nombres-dias">
                {["Lun", "Mar", "Mié", "Jue", "Vie", "Sáb", "Dom"].map((d) => (
                    <li key={d} className="nombre-dia">{d}</li>
                ))}
            </ul>

            <div className="grid-calendario">
                {dias.map((dia) => {
                    const fechaStr = format(dia, "yyyy-MM-dd");
                    const dataDia = datosCalendario[fechaStr];
                    return (
                        <CasillaDia
                            key={dia.toISOString()}
                            fecha={dia}
                            esMesActual={isSameMonth(dia, mesActual)}
                            esHoy={isToday(dia)}
                            esFuturo={isAfter(dia, new Date())}
                            emociones={dataDia?.emociones_primarias || []}
                            actividades={dataDia?.actividades_preview || []}
                        />
                    )
                })}
            </div>
            <ButtonGroup>
                <Button texto='Ver estadísticas' to='#' />
                <Button texto='Registro diario' to='/mis-emociones/registro-emocion' />
            </ButtonGroup>
        </section>
    );
};
