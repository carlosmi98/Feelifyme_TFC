import { Link } from "react-router-dom";
import './Boton.css'
const Boton = ({ texto, to }) => {

    return <>
        <Link to={ to } className="botones-generales">{ texto }</Link>
    </>
}

export default Boton