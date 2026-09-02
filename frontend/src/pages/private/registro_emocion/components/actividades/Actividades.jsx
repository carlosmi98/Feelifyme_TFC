import { useActividades } from "../../../../../hooks/useActividades";
import { useEmotionalAssets } from "../../../../../hooks/useEmotionalAssets";
import { Title } from "../../../../../componentes/generales";
import './actividades.css'

const CATEGORIAS_META = {
    fisica:     { label: "Física",      emoji: "🏃" },
    bienestar:  { label: "Bienestar",   emoji: "🌿" },
    creativa:   { label: "Creativa",    emoji: "🎨" },
    digital:    { label: "Digital",     emoji: "💻" },
    productiva: { label: "Productiva",  emoji: "🧠" },
    social:     { label: "Social",      emoji: "🤝" },
    cotidiana:  { label: "Cotidiana",   emoji: "📋" },
};

const ORDEN_CATEGORIAS = ["fisica", "bienestar", "creativa", "digital", "productiva", "social", "cotidiana"];

export const Actividades = ({ seleccionadasActuales, onSelectActividades }) => {
    const { actividades, loading, error } = useActividades();
    const { getActivityIcon } = useEmotionalAssets();

    const toggle = (id) => {
        const updated = seleccionadasActuales.includes(id)
            ? seleccionadasActuales.filter(x => x !== id)
            : [...seleccionadasActuales, id];
        onSelectActividades(updated);
    };

    if (loading) return <div className="cargando">Cargando actividades...</div>;
    if (error) return <div className="error">No se pudieron cargar las actividades.</div>;

    // Agrupar por categoría
    const porCategoria = actividades.reduce((acc, act) => {
        const cat = act.categoria || "cotidiana";
        if (!acc[cat]) acc[cat] = [];
        acc[cat].push(act);
        return acc;
    }, {});

    // Respetar el orden definido, ignorar categorías sin actividades
    const categoriasOrdenadas = ORDEN_CATEGORIAS.filter(c => porCategoria[c]?.length > 0);

    return (
        <section className="contenedor-actividades">
            <Title nivel={2} className="titulo-actividades">Actividades</Title>

            {categoriasOrdenadas.map(cat => {
                const { label, emoji } = CATEGORIAS_META[cat] ?? { label: cat, emoji: "📌" };
                return (
                    <div key={cat} className="categoria-grupo">
                        <h3 className="categoria-titulo">
                            <span className="categoria-emoji">{emoji}</span>
                            {label}
                        </h3>
                        <ul className="actividades-lista">
                            {porCategoria[cat].map(act => (
                                <li
                                    key={act.id}
                                    className={`actividad-item ${seleccionadasActuales.includes(act.id) ? 'seleccionada' : ''}`}
                                    onClick={() => toggle(act.id)}
                                >
                                    <img
                                        src={getActivityIcon(act.nombre)}
                                        alt={act.nombre}
                                        className="actividad-item-img"
                                    />
                                    <span className="titulo-texto">{act.nombre.replace(/_/g, ' ')}</span>
                                </li>
                            ))}
                        </ul>
                    </div>
                );
            })}
        </section>
    );
};
