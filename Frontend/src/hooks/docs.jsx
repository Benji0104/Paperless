import { useState } from 'react';


function Docs() {

     const [archivos, setArchivos] = useState([]);
    const lista = async () => {
    try {
        const response = await fetch('http://localhost:8000/auth/archivos', {
        method: 'GET',
        credentials: "include",
        headers: {
            'Authorization': `Bearer ${localStorage.getItem('access_token')}`,
            'Content-Type': 'application/json',
            
        },

        });

        if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.message || 'Error al obtener la lista de archivos');
        }

        const data = await response.json();
        console.log('✅ Datos recibidos en lista():', data); // DEBUG
        return data;

    } catch (error) {
        console.error('Error en lista():', error);
        throw error;
    }
        };
        return { lista, archivos };
}

export { Docs };