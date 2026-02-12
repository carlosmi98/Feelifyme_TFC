import { Link } from "react-router-dom"
import { useEffect } from "react"
import logo from '../../../assets/images/menu/logo.PNG'
import acceso from '../../../assets/images/menu/acceso.png'
import './nav.css'


const Nav = () => {
    return (
        <>
            <Link to='/'>
                <img src={ logo } alt='logo' className="logo-nav" />
            </Link>

            <input type="checkbox" id="menu-hamb"/>
            <label htmlFor="menu-hamb" className="hamburguesa"></label>

            <nav className="nav">
                <ul className="lista-menu">
                    <li><Link to="/">Inicio</Link></li>
                    <li><Link to="/sobre-nosotros">Sobre Nosotros</Link></li>
                    <li><Link to="/como-funciona">Cómo Funciona</Link></li>
                    <li><Link to="/curiosidades">Curiosidades</Link></li>
                    <li><Link to="/contacto">Contacto</Link></li>
                </ul>
            </nav>

            <Link to="/acceso" className="acceso-img">
                <img src={acceso} alt='acceso' />
            </Link>
        </>
    )
}

export default Nav