import { useState } from "react";
import "./pregunta_iteractiva.css"

import GrupoBotones from "../generales/grupo-botones/GrupoBotones";
import Boton from "../generales/botons/Boton";

const PreguntaIteractiva = () => {
    const [mensaje, setMensaje] = useState("");
    const [emocionSeleccionada, setEmocionSeleccionada] = useState(null)

    const mensajes = {
        bien: "Nos alegra que estés bien pero siempre puedes darle una oportunidad a FeelifyMe.",
        neutro: "FeelifyMe te puede ayudar a abrirte al mundo de las emociones.",
        mal: "Usa FeelifyMe para ver patrones en tus conductas, estamos contigo."
        }

    const emociones = ['bien', 'neutro', 'mal']

    const mostrarMensaje = (emocion) => {
        setEmocionSeleccionada(emocion)
        setMensaje(mensajes[emocion])
    }

    return (
        <div className="estado-emocional">
            <h3>¿Cómo te sientes hoy?</h3>
            <div className="botonesIteractivos">
                {emociones.map((emocion) => (
                <button key={emocion} onClick={() => mostrarMensaje(emocion)} className={emocion === emocionSeleccionada ? `btn-${emocion}` : 'btn-base'}>
                    {emocion} 
                </button>
                ))}
            </div>
            {/* Renderizado condicional: solo muestra el mensaje si existe */}
            {mensaje && <p>{mensaje}</p>}
            <GrupoBotones>
                <Boton texto = 'Registrarme' to='#' />
            </GrupoBotones>
        </div>
    )
}

export default PreguntaIteractiva;