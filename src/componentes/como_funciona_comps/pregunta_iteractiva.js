import { useState } from "react";

const Emocion = () => {
    const [mensaje, setMensaje] = useState("");

    const mensajes = {
        bien: "Nos alegra que estés bien pero siempre puedes darle una oportunidad a FeelifyMe.",
        neutro: "FeelifyMe te puede ayudar a abrirte al mundo de las emociones.",
        mal: "Usa FeelifyMe para ver patrones en tus conductas, estamos contigo."
        }

    const emociones = ['bien', 'neutro', 'mal']

    const mostrarMensaje = (emocion) => {
        setMensaje(mensajes[emocion])
    }

    return (
        <div className="estado-emocional">
        <h3>¿Cómo te sientes hoy?</h3>
        <div className="botones">
            {emociones.map((emocion) => (
            <button key={emocion} onClick={() => mostrarMensaje(emocion)}>
                {emocion} 
            </button>
            ))}
        </div>
        {/* Renderizado condicional: solo muestra el mensaje si existe */}
        {mensaje && <p>{mensaje}</p>}
        </div>
    )
}

export default Emocion;