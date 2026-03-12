import { useEffect } from "react"

import SeccionesSobreNosotros from "../../componentes/sobre_nosotros/SeccionesSobreNosotros"

const SobreNosotros = () => {
    useEffect(() => {
        document.title = 'Sobre nosotros'
    })
    return <>
        <SeccionesSobreNosotros />
    </>
}

export default SobreNosotros;