import { useParams, useNavigate } from "react-router-dom";
import { format, parseISO } from "date-fns";
import { es } from "date-fns/locale";
import "./ResumenCronologico.css";
import { useEmotionalAssets } from "../../../../../hooks/useEmotionalAssets";
import { useResumenDiario } from "../../../../../hooks/useResumenDiario";

export const ResumenCronologico = () => {
    const { fecha } = useParams();
    const navigate = useNavigate();
    const { getEmocionColor, getActivityIcon } = useEmotionalAssets();
    const { resumen, loading } = useResumenDiario(fecha);

    if (loading) return <div className="resumen-feedback">Cargando...</div>;
    if (!resumen || resumen.registros.length === 0) return <div className="resumen-feedback">No hay registros para este día.</div>;

    const fechaTxt = format(parseISO(fecha), "EEEE, d 'de' MMMM", { locale: es });

    return (
        <section className="resumen-cronologico-container">
            <header className="resumen-header">
                <button onClick={() => navigate("/mis-emociones")} className="btn-back"> ← Volver </button>
                <h1>{fechaTxt.charAt(0).toUpperCase() + fechaTxt.slice(1)}</h1>
            </header>

            <div className="lista-registros">
                {resumen.registros.map(reg => (
                    <article key={reg.id} className="tarjeta-registro">
                        <div className="hora-badge">{reg.hora.substring(0, 5)}</div>

                        <div className="contenido-registro">
                            <div className="grupo">
                                <strong>Emociones:</strong>
                                <div className="chips">
                                    {reg.emociones.map(e => (
                                        <span key={e.id} className="chip" style={{ border: `2px solid ${getEmocionColor(e.nombre)}` }}>
                                            {e.nombre}
                                        </span>
                                    ))}
                                </div>
                            </div>

                            <div className="grupo">
                                <strong>Actividades:</strong>
                                <div className="iconos">
                                    {reg.actividades.map(a => (
                                        <img key={a.id} src={getActivityIcon(a.nombre)} alt={a.nombre} className="img-actividad" />
                                    ))}
                                </div>
                            </div>

                            {reg.notas && <p className="nota">"{reg.notas}"</p>}
                        </div>
                    </article>
                ))}
            </div>
        </section>
    );
};