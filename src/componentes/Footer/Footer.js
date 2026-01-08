import { Link } from "react-router-dom"

import instagram from "./images/instagram.png"
import linkedin from "./images/linkdlin.png"
import twitter from "./images/twitter.png"
import youtube from "./images/youtube.png"
import logo from "./images/logo.PNG"
import "./Footer.css"

const Footer = () => {

    const enlaces = [
        {texto:'Contacto', url:'/contacto'},
        {texto:'Mapa web', url:'/mapa'},
        { texto: 'Aviso legal y política de privacidad', url: '/legal' },
        { texto: 'Gestión de cookies', url: '/cookies' }
    ]

    const redes = [
        {src: instagram, alt: 'Instagram', url:'https://instagram.com/feelifyme'},
        { src: linkedin, alt: "LinkedIn", url: "https://linkedin.com/company/feelifyme" },
        { src: twitter, alt: "Twitter", url: "https://twitter.com/feelifyme" },
        { src: youtube, alt: "YouTube", url: "https://youtube.com/@feelifyme" }
    ]

    return <footer>
        <div className="menu-imagen">
            <div className="menu-footer">
                {enlaces.map(enlace => (
                    <Link key={enlace.texto} to={enlace.url} className="enlaces-footer">
                        {enlace.texto}
                    </Link>
                ))}
            </div>
            <img src={logo} alt="logo" className="logo-footer" />
        </div>
        <div className="contacto-redes">
            <div className="contacto">
                <p>FeelifyMe</p>
                <p>Calle Urganza 4, 12007 Castellón</p>
                <p>feelifyMe@gmail.com</p>
                <p>981845689</p>
            </div>
            <div className="redes">
                {redes.map(red =>(
                    <a key={red.alt} href={red.url} target="_blank" rel="noopener noreferrer">
                        <img src={red.src} alt={red.alt} className="img-red" />
                    </a>
                ))}
            </div>
        </div>
        <p className="copyright">&copy; 2025 FeelifyMe. Todos los derechos reservados.</p>
    </footer>
}

export default Footer