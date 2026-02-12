import imagenPrincipal from "../../assets/images/inicio/hero/imagenPrincipal.png"
import { Link } from "react-router-dom"
import "./Hero.css"
const Hero = () => {

    return <section className="principal">
                    <div className="contenido-texto">
                        <h1>Aprende a gestionar tus emociones. Mejora día a día con <span className="marca">FeelifyMe</span>.</h1>
                        <p className="parrafo-h1">Comparte cómo te sientes cada día. No estás solo: tanto en los momentos difíciles como en los buenos, estamos contigo. En <span className="marca">FeelifyMe</span> te ayudamos a comprender tus emociones y te ofrecemos consejos prácticos para aprender a gestionarlas con mayor claridad y equilibrio.</p>
                        <div className="botones-acceso">
                            <Link to="#" className="botones-generales">Iniciar sesión</Link>
                            <Link to="#" className="botones-generales">Crear cuenta</Link>
                        </div>
                    </div>
                    <div className="contenedor-imagen-principal">
                        <img src={ imagenPrincipal } className="img-principal" />
                    </div>

            </section>
}

export default Hero