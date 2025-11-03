import { useNavigate } from 'react-router-dom';
import '../styles/Login.css'; // Ruta del archivo CSS

const Login = () => {
    const navigate = useNavigate();

    const handleLogin = () => {
        navigate('/inicio');
    };

    return (

        <div className="login-bg d-flex justify-content-center align-items-center vh-100">
            <div className="login-box text-center">
                <h2 className="mb-4">Iniciar sesión con Google</h2>
                <button className="btn btn-light p-2" onClick={handleLogin}>
                    <img
                        src="/google-logo.png"
                        alt="Google logo"
                        style={{ width: '24px', height: '24px' }}
                    />
                </button>

            </div>
        </div>
    );
};

export default Login;