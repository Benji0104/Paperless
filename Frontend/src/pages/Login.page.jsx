import { useNavigate } from 'react-router-dom';
import '../styles/Login.css'; // Ruta del archivo CSS
import { useAuth } from '../hooks/useAuth';

const Login = () => {
    const navigate = useNavigate();
    const { registroWithGoogle} = useAuth();


    const handleRegistro = () => {
       registroWithGoogle();
    };

    return (

        <div className="login-bg d-flex justify-content-center align-items-center vh-100">
            <div className="login-box text-center">
                <h2 className="mb-4">Bienvenido a tu biblioteca web</h2>
                
                
                <button onClick={handleRegistro}>
                    <img
                        src="/registrarse.png"
                        alt="Google logo"
                       
                    />
                </button>

                <button  onClick={handleRegistro}>
                    <img
                        src="/Iniciar_sesion.png"
                        alt="Google logo"

                    />
                </button>


            </div>
        </div>
    );
};

export default Login;