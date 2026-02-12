import { useEffect } from "react";

import Hero from "../../componentes/inicio/hero/Hero";
import Descubre from "../../componentes/inicio/descubre/Descubre";
import Beneficios from "../../componentes/inicio/beneficios/Beneficios";


function Inicio() {
    useEffect(() => {
        document.title = 'Inicio'
    })
    return (
        <>
            <Hero />
            <Descubre />
            <Beneficios />
        </>
    );
}

export default Inicio;
