import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';

const Validar = () => {
    const navigate = useNavigate();
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        const urlParams = new URLSearchParams(window.location.search);
        
        const success = urlParams.get('success');
        const errorParam = urlParams.get('error');
        const token = urlParams.get('token');
        const email = urlParams.get('email');
        const name = urlParams.get('name');
        const picture = urlParams.get('picture');

        if (errorParam) {
            setError(errorParam);
            setLoading(false);
            console.error('❌ Error de autenticación:', errorParam);
            return;
        }

        if (success === 'true' && token) {
            // Guardar datos del usuario
            localStorage.setItem('access_token', token);
            localStorage.setItem('user_email', email);
            localStorage.setItem('user_name', name);
            localStorage.setItem('user_picture', picture);

            console.log('✅ Autenticación exitosa');
            console.log('Usuario:', { email, name });
            console.log('Token:', token);
            console.log('Foto:', picture);
            console.log('Redirigiendo al dashboard...');
            
            // Limpiar URL
            window.history.replaceState({}, '', window.location.pathname);
            
            // Redirigir al dashboard
            navigate('/inicio');
        } else {
            setError('No se recibieron datos válidos');
            setLoading(false);
        }
    }, []);

    return (
        <div className="login-bg d-flex justify-content-center align-items-center vh-100">
            <div className="login-box text-center">
                <h2 className="mb-4">Bienvenido a tu biblioteca web</h2>
                {loading ? (
                    <h1>VALIDANDO LAS CREDENCIALES...</h1>
                ) : (
                    <div>
                        <h1 className="text-danger">Error</h1>
                        <p>{error}</p>
                        <button onClick={() => navigate('/login')}>
                            Volver a intentar
                        </button>
                    </div>
                )}
            </div>
        </div>
    );
};

export default Validar;