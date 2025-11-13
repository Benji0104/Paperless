import React, { useEffect, useState } from "react";
import CargaMensaje from "../components/cargar.jsx";
import ErrorMensaje from "../components/error.jsx";

const Perfil = () => {
    const [perfilData, setPerfilData] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        const obtenerPerfil = async () => {
            try {
                setLoading(true);
                const token = localStorage.getItem('access_token');
                
                if (!token) {
                    throw new Error('No hay token de acceso');
                }

                const response = await fetch('http://localhost:8000/auth/perfil', {
                    method: 'GET',
                    credentials: 'include',
                    headers: {
                        'Authorization': `Bearer ${token}`,
                        'Content-Type': 'application/json',
                    },
                });

                if (!response.ok) {
                    throw new Error(`Error al obtener el perfil: ${response.status}`);
                }

                const data = await response.json();
                console.log('Datos del perfil:', data);
                setPerfilData(data);
                
            } catch (err) {
                console.error('Error:', err);
                setError(err.message);
            } finally {
                setLoading(false);
            }
        };

        obtenerPerfil();
    }, []);

    if (loading) {
        return (
            <CargaMensaje mensaje="Cargando perfil de usuario..." />
        );
    }

    if (error) {
        return (
           <ErrorMensaje tituloM="Error al cargar el perfil" mensaje={error} />
        );
    }

    return (
        <div className="container mt-5">
            <h1>Perfil de Usuario</h1>
            {perfilData ? (
                <div className="card">
                    <div className="card-body">
                        <h5 className="card-title">Información del Perfil</h5>
                        <pre>{JSON.stringify(perfilData, null, 2)}</pre>
                        {/* Aquí puedes mostrar los datos específicos:
                        <p><strong>Nombre:</strong> {perfilData.nombre}</p>
                        <p><strong>Email:</strong> {perfilData.email}</p>
                        */}
                    </div>
                </div>
            ) : (
                <p>No se encontraron datos del perfil</p>
            )}
        </div>
    );
};

export default Perfil;