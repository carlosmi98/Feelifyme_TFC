import { Link } from "react-router-dom";
import './Boton.css'
const Boton = ({ texto, to }) => {

    return <div className="botones">
        <Link to={ to } className="botones-generales">{ texto }</Link>
    </div>
}

export default Boton