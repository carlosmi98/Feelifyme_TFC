import { useState } from 'react';
import './FormularioContacto.css'

const FormularioContacto = () => {

    const [form, setForm] = useState({
        nombre: '',
        correo: '',
        asunto: '',
        mensaje: ''
        })

    const onChange = (e) => { 
        setForm({ ...form, [e.target.name]: e.target.value 

        })
    }

    const onSubmit = (e) => { 
        e.preventDefault()
        console.log("Datos enviados:", form)
    }


    return <form onSubmit={onSubmit} className="form">
        <div className="conjunto">
            <label htmlFor="nombre">Nombre</label>
            <input type="text" id="nombre" name="nombre" value={form.nombre} onChange={onChange} placeholder="Ruth" />
        </div>

        <div className="conjunto">
            <label htmlFor="correo">Correo electrónico</label>
            <input type="email" id="correo" name="correo" value={form.correo} onChange={onChange} placeholder="ruth@gmail.com" />
        </div>

        <div className="conjunto">
            <label htmlFor="asunto">Asunto</label>
            <input type="text" id="asunto" name="asunto" value={form.asunto} onChange={onChange} placeholder="Escribe el motivo" />
        </div>

        <div className="conjunto">
            <label htmlFor="mensaje">Mensaje</label>
            <textarea id="mensaje" name="mensaje" value={form.mensaje} onChange={onChange}></textarea>
        </div>

        <button type="submit">Enviar</button>
    </form>
}

export default FormularioContacto