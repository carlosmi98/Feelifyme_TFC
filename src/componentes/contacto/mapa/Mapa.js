import './Mapa.css'

const Mapa = () => {
    return (
        <iframe
        title="Mapa con la ubicación de FeelifyMe"
        className="iframe"
        src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3082.123456789!2d-0.123456!3d39.987654!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x0%3A0x0!2sCalle%20Urganza%204%2C%20Castell%C3%B3n!5e0!3m2!1ses!2ses!4v1234567890"
        allowFullScreen
        loading="lazy"
        ></iframe>
    )
}

export default Mapa;
