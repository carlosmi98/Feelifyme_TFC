import { Link } from "react-router-dom"
import { useEffect } from "react"
import logo from '../images/logo.PNG'
import acceso from '../images/acceso.png'
import './nav.css'


const Nav = () => {
    return (
        <header>
            <Link to='/'>
                <img src={ logo } alt='logo' className="logo-nav" />
            </Link>

            <input type="checkbox" id="menu-hamb"/>
            <label htmlFor="menu-hamb" className="hamburguesa">☰</label>

            <nav>
                <ul className="lista-menu">
                    <li><Link to="/">Inicio</Link></li>
                    <li><Link to="/sobre-nosotros">Sobre Nosotros</Link></li>
                    <li><Link to="/como-funciona">Cómo Funciona</Link></li>
                    <li><Link to="/curiosidades">Curiosidades</Link></li>
                    <li><Link to="/contacto">Contacto</Link></li>
                </ul>
            </nav>

            <Link to="/acceso">
                <img src={acceso} alt='acceso' className="acceso-img" />
            </Link>
        </header>
    )
}

export default Nav