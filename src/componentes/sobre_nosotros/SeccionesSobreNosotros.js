import Card from "../generales/cards/Card"

const SeccionesSobreNosotros = () => {

    const seccionesSobreNosotros = [
        {
            id: 1,
            title: "Propósito",
            description: [
                "FeelifyMe nace para ayudarte a registrar, entender y cuidar tus emociones de forma sencilla, visual y empática. Queremos que cada persona tenga un espacio seguro donde pueda conectar consigo misma, sin juicios ni complicaciones. Porque tus emociones importan, y mereces una herramienta que te acompañe en cada paso de tu bienestar emocional."
            ],
        },
        {
            id: 2,
            title: "Origen",
            description: [
                "FeelifyMe nació de una inquietud muy concreta: la necesidad de tener un espacio donde poder expresar cómo te sientes sin complicaciones. No fue una idea pensada para grandes audiencias, sino una solución personal que poco a poco fue tomando forma. Con el tiempo, se convirtió en un proyecto con intención clara: ofrecer una herramienta emocionalmente amable, visual y accesible, que acompañe a las personas en su día a día."
            ],
        },
        {
            id: 3,
            title: "¿Quién está detrás de FeelifyMe?",
            description: [
                "FeelifyMe es un proyecto personal creado con dedicación y propósito. Detrás de cada pantalla, diseño y funcionalidad hay una sola persona: alguien que cree profundamente en la importancia de cuidar la salud emocional. Aunque aún está en desarrollo, la visión es clara: construir una herramienta accesible, visual y empática que acompañe a las personas en su día a día."
            ],
        },
        {
            id: 4,
            title: "¿Hacia dónde vamos?",
            description: [
                "Queremos que FeelifyMe evolucione contigo, acompañándote en cada paso de tu bienestar emocional. En el futuro, imaginamos una plataforma capaz de ofrecerte apoyo emocional inteligente, donde herramientas basadas en IA puedan conversar contigo, entender tus registros, y ofrecerte recomendaciones personalizadas en tiempo real.",
                
                "Desde ayudarte a reflexionar sobre lo que sientes, hasta sugerirte acciones concretas según tu estado emocional, el objetivo es que FeelifyMe se convierta en un compañero emocional cotidiano, accesible, empático y cada vez más intuitivo. Porque tu bienestar no es estático, y nosotros tampoco lo seremos.",
            ]
        }
    ]

    return <>
        <h1>Creemos que entender cómo te sientes es el primer paso para cuidarte.</h1>

        <section class="info-sobre-nosotros">
            {seccionesSobreNosotros.map(c => (
                <Card card= {c} />
            ))}
        </section>
    </>
}

export default SeccionesSobreNosotros