import { Outlet, useOutletContext } from "react-router-dom"
import Nav from "../componentes/Menu/public/Nav"
import Footer from "../componentes/Footer/Footer"
import "../styles/layout.css"

const PublicLayout = () => {

    return <div className="estructura">
        <header>
            <Nav />
        </header>
        <main>
            <Outlet />
        </main>
        <Footer />
    </div>
}

export default PublicLayout