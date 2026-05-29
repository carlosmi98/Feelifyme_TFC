import { Link, NavLink } from "react-router-dom"
import { useAuth } from "../../../context/AuthContext"
import { iconoLogo } from '../../../assets/images/menu'
import { iconoLogout } from '../../../assets/images/private/menu'

export const PrivateNav = () => {
    const { logout } = useAuth();

    return (
        <>
            <Link to='/'>
                <img src={iconoLogo} alt='logo' className="logo-nav" />
            </Link>

            <input type="checkbox" id="menu-hamb" />
            <label htmlFor="menu-hamb" className="hamburguesa"></label>

            <nav className="nav">
                <ul className="lista-menu">
                    <li><NavLink to="/" className={({ isActive }) => (isActive ? "activo" : "")}>Inicio</NavLink></li>
                    <li><NavLink to="/mis-emociones" className={({ isActive }) => (isActive ? "activo" : "")}>Mis emociones</NavLink></li>
                    <li><NavLink to="/evolucion" className={({ isActive }) => (isActive ? "activo" : "")}>Mi evolución</NavLink></li>
                    <li><NavLink to="/recomendaciones" className={({ isActive }) => (isActive ? "activo" : "")}>Recomendaciones</NavLink></li>
                    <li><NavLink to="/logros" className={({ isActive }) => (isActive ? "activo" : "")}>Logros</NavLink></li>
                    <li><NavLink to="/perfil" className={({ isActive }) => (isActive ? "activo" : "")}>Perfil</NavLink></li>
                </ul>
            </nav>

            <button onClick={logout} className="boton-logout" title="Cerrar sesión">
                <img src={iconoLogout} alt='logout' />
            </button>
        </>
    )
}