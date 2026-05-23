import React, { useState } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { updateProfile } from '../../../../../services/authService';
import { SectionCard } from '../../../../../componentes/generales';
import { Title } from '../../../../../componentes/generales';
import './EditarPerfilContainer.css';

export const EditarPerfilContainer = () => {
    const navigate = useNavigate();
    const location = useLocation();
    
    // Obtenemos los datos pasados por navegación, o inicializamos vacíos si el usuario entró directo por URL
    const initialProfile = location.state?.userProfile || {
        email: '',
        profile: { nombre: '', apellido1: '', apellido2: '' }
    };

    const [formData, setFormData] = useState({
        nombre: initialProfile.profile?.nombre || '',
        apellido1: initialProfile.profile?.apellido1 || '',
        apellido2: initialProfile.profile?.apellido2 || '',
        email: initialProfile.email || ''
    });

    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');

    const handleChange = (e) => {
        setFormData({
            ...formData,
            [e.target.name]: e.target.value
        });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setLoading(true);
        setError('');

        try {
            await updateProfile({
                email: formData.email,
                profile: { 
                    nombre: formData.nombre, 
                    apellido1: formData.apellido1,
                    apellido2: formData.apellido2
                }
            });
            alert("Perfil actualizado correctamente");
            navigate('/perfil'); // Volver al perfil
        } catch (err) {
            console.error(err);
            setError('Error al actualizar el perfil. Revisa los datos.');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="layout-page">
            <Title nivel={1} className="titulo-principal text-center">Editar Perfil</Title>
            
            <div className="editar-perfil-container">
                <SectionCard>
                    <form onSubmit={handleSubmit} className="formulario-edicion">
                        {error && <p style={{ color: 'red', textAlign: 'center' }}>{error}</p>}

                        <div className="form-group">
                            <label htmlFor="nombre">Nombre</label>
                            <input 
                                type="text" 
                                id="nombre" 
                                name="nombre" 
                                value={formData.nombre} 
                                onChange={handleChange} 
                                required 
                            />
                        </div>

                        <div className="form-group">
                            <label htmlFor="apellido1">Primer Apellido</label>
                            <input 
                                type="text" 
                                id="apellido1" 
                                name="apellido1" 
                                value={formData.apellido1} 
                                onChange={handleChange} 
                                required 
                            />
                        </div>

                        <div className="form-group">
                            <label htmlFor="apellido2">Segundo Apellido</label>
                            <input 
                                type="text" 
                                id="apellido2" 
                                name="apellido2" 
                                value={formData.apellido2} 
                                onChange={handleChange} 
                            />
                        </div>

                        <div className="form-group">
                            <label htmlFor="email">Email</label>
                            <input 
                                type="email" 
                                id="email" 
                                name="email" 
                                value={formData.email} 
                                onChange={handleChange} 
                                required 
                            />
                        </div>

                        <div className="botones-formulario">
                            <button type="button" className="btn-cancelar" onClick={() => navigate('/perfil')}>
                                Cancelar
                            </button>
                            <button type="submit" className="btn-guardar" disabled={loading}>
                                {loading ? 'Guardando...' : 'Guardar Cambios'}
                            </button>
                        </div>
                    </form>
                </SectionCard>
            </div>
        </div>
    );
};
