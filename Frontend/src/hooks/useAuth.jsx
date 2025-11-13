import { useState } from 'react';
import { useNavigate } from 'react-router-dom';

const API_URL = 'http://localhost:8000/'; 

function useAuth() {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [files, setFiles] = useState(null);
  const navigate = useNavigate();

  {/* Registro */}
  const registroWithGoogle = async () => {
    window.location.href = `${API_URL}auth/registro`;
 
  };

  const getAccessToken = () => localStorage.getItem('access_token');//obtiene token

  const LoginWithGoogle = async () => {
    window.location.href = `${API_URL}auth/login`;
  }

  {/* cerrar sesion*/}
  const logout = () => {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    navigate('/login');
  };

  {/* Convertir los archivos */}
  const convertFiles = async (filesToConvert) => {
  const formData = new FormData();
  filesToConvert.forEach((file) => {
    formData.append('files', file);
  });

  const response = await fetch(`${API_URL}Docs/`, {
    method: 'POST',
    headers: {
      Authorization: `Bearer ${getAccessToken()}`,
    },
    body: formData,
  });

  if (!response.ok) throw new Error('Error en la conversión');
    const data = await response.json();

    return data.resultados || [];
};


  return {
    convertFiles,
    registroWithGoogle,
    getAccessToken,
    logout,
    loading,
    error,
    files
  };
}

export { useAuth };
