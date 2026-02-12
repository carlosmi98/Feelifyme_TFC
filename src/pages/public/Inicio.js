import Hero from "../../componentes/inicio/Hero";
import { useEffect } from "react";

function Inicio() {
    useEffect(() => {
        document.title = 'Inicio'
    })
    return (
        <>
            <Hero />
        </>
    );
}

export default Inicio;
