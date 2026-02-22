import imagenPrincipal from "../../../assets/images/inicio/hero/imagenPrincipal.png"
import { Link } from "react-router-dom"
import "./Hero.css"
import GrupoBotones from "../../generales/grupo-botones/GrupoBotones"
import Boton from "../../generales/botons/Boton"


const Hero = () => {

    return <section className="principal">
                    <div className="contenido-texto">
                        <h1>Aprende a gestionar tus emociones. Mejora día a día con <span className="marca">FeelifyMe</span>.</h1>
                        <p className="parrafo-h1">Comparte cómo te sientes cada día. No estás solo: tanto en los momentos difíciles como en los buenos, estamos contigo. En <span className="marca">FeelifyMe</span> te ayudamos a comprender tus emociones y te ofrecemos consejos prácticos para aprender a gestionarlas con mayor claridad y equilibrio.</p>

                        <GrupoBotones>
                            <Boton texto = 'Iniciar sesion' to='#' />
                            <Boton texto = 'Crear cuenta' to='#' />
                        </GrupoBotones>
                    </div>
                    <div className="contenedor-imagen-principal">
                        <img src={ imagenPrincipal } className="img-principal" />
                    </div>

            </section>
}

export default Hero