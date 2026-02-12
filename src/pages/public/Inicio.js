import Hero from "../../componentes/inicio/hero/Hero";
import Descubre from "../../componentes/inicio/descubre/Descubre";

import { useEffect } from "react";

function Inicio() {
    useEffect(() => {
        document.title = 'Inicio'
    })
    return (
        <>
            <Hero />
            <Descubre />
        </>
    );
}

export default Inicio;
