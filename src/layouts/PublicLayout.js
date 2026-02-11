import { Outlet, useOutletContext } from "react-router-dom"
import Nav from "../componentes/Menu/public/Nav"
import Footer from "../componentes/Footer/Footer"


const PublicLayout = () => {

    return <>
        <Nav />
        <main>
            <Outlet />
        </main>
        <Footer />
    </>
}

export default PublicLayout