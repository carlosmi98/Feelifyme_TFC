import "./Card.css"

const Card = ({ card }) => {

    return <article className="tarjetas-generales">
        <h3>
            {card.imagen && <img src={card.imagen} className="ico"/>}
            { card.title }
        </h3>
        <p>{ card.description }</p>
    </article>
}

export default Card