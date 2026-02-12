import grafico from "../../../assets/images/inicio/beneficios/iconEstad.png"
import calendario from "../../../assets/images/inicio/beneficios/iconCal48.PNG"
import reflexion from "../../../assets/images/inicio/beneficios/reflex.png"
import logro from "../../../assets/images/inicio/beneficios/logro.png"
import privacidad from"../../../assets/images/inicio/beneficios/priv.png"
import sugerencia from "../../../assets/images/inicio/beneficios/sugeren.png"

import Card from "../../generales/cards/Card"

import "./Beneficios.css"

const Beneficios = () => {
    const tarjetas = [
        {
            imagen: calendario,
            title: 'Calendario de emociones',
            description: 'Cada día registra tus emociones y observa tu evolución de forma sencilla y visual. Podrás identificar patrones y ver cómo cambian tus estados de ánimo a lo largo del tiempo.'
        },

        {
            imagen: grafico,
            title: 'Gráficos de progreso',
            description: 'Visualiza estadísticas semanales y mensuales para entender tus patrones emocionales. Gráficos claros te ayudarán a detectar tendencias y a reflexionar sobre tu bienestar.'
        },
        {
            imagen: sugerencia,
            title: 'Recomendaciones',
            description: 'Recibe sugerencias y micro-tareas según cómo te hayas sentido cada día. Desde ejercicios de respiración hasta pequeños hábitos que fomenten tu equilibrio emocional.'
        },

        {
            imagen: logro,
            title: 'Rachas y logros',
            description: 'Celebra tu constancia y motívate con medallas y puntos de progreso. Cada registro cuenta y te anima a mantener hábitos saludables en tu rutina que te ayudarán.'
        },
        {
            imagen: reflexion,
            title: 'Reflexión diaria',
            description: 'Espacios cortos para escribir notas, pensamientos o aprendizajes del día. Una manera de conectar contigo mismo y mejorar tu autoconciencia emocional.'
        },

        {
            imagen: privacidad,
            title: 'Privacidad y control',
            description: 'Tus datos son solo tuyos. Podrás exportarlos, revisarlos o eliminarlos cuando quieras, garantizando que tu información esté siempre bajo tu control.'
        }
    ]

    return <section className="beneficios">
        <h2>Beneficios</h2>
        <div className="contenedor-general">
            {tarjetas.map((t) => {
                return <Card card={t} />
            })}
        </div>
    </section>

}

export default Beneficios