import Calendario from '../../assets/images/como_funciona/calendario.png'
import Estadisticas from '../../assets/images/como_funciona/estadisticas.png'
import Medallas from '../../assets/images/como_funciona/medallas.png'
import Recomendaciones from '../../assets/images/como_funciona/recomendaciones.png'
import Rueda from '../../assets/images/como_funciona/rueda3.jpg'
import "./SeccionesComoFunciona.css"

const SeccionesComoFunciona = () => {

    const secciones = [
        {
            id: 1,
            titulo: "Calendario",
            textoAntesLista: [
            "En FeelifyMe, el calendario te permite registrar cómo te sientes cada día de forma visual y sencilla. Al hacer clic en el día actual, accedes a una rueda de emociones donde puedes seleccionar todas las emociones que reflejen tu estado.",
            "Cada día queda guardado con un resumen emocional. Si has elegido varias emociones, podrás verlas completas al volver a entrar en ese día. Este sistema te ayuda a entender tu evolución emocional, identificar patrones y conectar contigo mismo."
            ],
            img: Calendario,
            alt: "calendario"
        },

        {
            id: 2,
            titulo: "Rueda de emociones",
            textoAntesLista: [
            "Al seleccionar el día en el calendario, se mostrará una rueda de emociones con múltiples opciones organizadas por categorías.",
            "Podrás elegir una o varias emociones que reflejen tu estado emocional en ese momento. No hay límite: si tu día ha sido complejo, puedes registrar todas las emociones que necesites.",
            "Una vez seleccionadas, quedarán guardadas en el calendario y podrás consultarlas en cualquier momento para reflexionar sobre tu evolución emocional."
            ],
            img: Rueda,
            alt: "rueda emocional"
        },

        {
            id: 3,
            titulo: "Gráficos",
            textoAntesLista: [
            "En la sección de Estadísticas de FeelifyMe, puedes visualizar tu evolución emocional a lo largo del tiempo. Tras registrar tus emociones día a día, el sistema genera gráficos que te ayudan a entender cómo te has sentido durante la semana o el mes:"
            ],
            lista: [
            "El gráfico de líneas muestra la variación de emociones como Alegría, Tristeza, Miedo, Ira, Sorpresa y Calma a lo largo de los días. Así puedes detectar picos, caídas o patrones repetitivos.",
            "El gráfico circular representa la distribución mensual de tus emociones, permitiéndote ver cuáles han predominado y cómo se equilibran entre sí."
            ],
            textoDespuesLista: [
            "Esta visualización te ofrece una forma sencilla y profunda de reflexionar sobre tu bienestar emocional, tomar conciencia de tus estados y avanzar hacia una mayor estabilidad personal."
            ],
            img: Estadisticas,
            alt: "estadisticas"
        },

        {
            id: 4,
            titulo: "Recomendaciones",
            textoAntesLista: [
            "Cada día, según las emociones que registres, FeelifyMe te ofrecerá tips personalizados para ayudarte a gestionarlas de forma saludable.",
            "Las sugerencias pueden incluir ejercicios de respiración, meditación, escribir lo que agradeces, salir a caminar, ir a una cafetería o conectar con alguien cercano.",
            "Junto a cada recomendación, tendrás la opción de añadir una breve reflexión personal: cómo te sentiste, qué aprendiste o qué te ayudó ese día.",
            "Además, podrás marcar si has completado el tip, lo que contribuirá a tu progreso emocional."
            ],
            img: Recomendaciones,
            alt: "recomendaciones",
            class: "imgComoFunciona"
        },

        {
            id: 5,
            titulo: "Logros",
            textoAntesLista: [
            "La sección de Logros te permite visualizar tu progreso emocional de forma positiva y motivadora. A medida que completas reflexiones, aplicas recomendaciones y mantienes constancia en el registro diario, vas desbloqueando medallas y reconocimientos que celebran tu compromiso con el bienestar."
            ],
            lista: [
            "Logros personales: muestra cuántas reflexiones has escrito, cuántos tips has aplicado y cuántos días seguidos has mantenido tu rutina emocional.",
            "Medallas por hitos: recompensas visuales que reconocen tu constancia, tu capacidad de introspección y tu esfuerzo diario."
            ],
            textoDespuesLista: [
            "Porque en FeelifyMe, cada pequeño paso cuenta. Y tu bienestar merece ser celebrado."
            ],
            img: Medallas,
            alt: "logros",
            class: "imgComoFunciona"
        }
    ]

    return <>
        <h1>Así te acompañamos cada día</h1>
        {secciones.map(s => (
            <section key={s.id} className='seccion'>
                <div className='texto'>
                    <h2>{ s.titulo }</h2>
                    {s.textoAntesLista.map(p => (
                        <p className='parrafoSeccionesComoFunciona'>{ p }</p>
                    ))}
                    {s.lista?.map((l, i) => (
                        <ul>
                            <li key={ i } className='listaComoFunciona'>{ l }</li>
                        </ul>
                    ))}
                    {s.textoDespuesLista?.map((p, i) => (
                        <p key={ i }>{ p }</p>
                    ))}
                </div>
                <img src={s.img} alt={s.alt} className= "imgComoFunciona" />
            </section>
        ))}
    </>
}

export default SeccionesComoFunciona