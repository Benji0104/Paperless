
import { ReactReader } from 'react-reader'
import { useState, useEffect } from 'react'
import { useParams, useLocation } from 'react-router-dom'

const Visor = () => {
  const { id } = useParams();
  const location = useLocation();
  const [locationState, setLocationState] = useState(null)
  const [epubUrl, setEpubUrl] = useState(null)

  useEffect(() => {
    // Obtener el ID de diferentes fuentes

    const id_file = id 
    
    console.log('ID de ruta:', id);
    console.log('token'+localStorage.getItem('access_token'))
    if (!id_file) {
      console.error('No se proporcionó id en la URL');
      return;
    }


    const fetchData = async () => {
      try {
        const response = await fetch(`http://localhost:8000/auth/descarga/${id_file}`, {
          method: 'GET',
          credentials: 'include',
          headers: {
            Authorization: `Bearer ${localStorage.getItem('access_token')}`,
            
          },
        });

        if (!response.ok) {
          throw new Error(`Error al descargar el archivo: ${response.status}`);
        }

        const blob = await response.blob();
        const fileURL = URL.createObjectURL(blob);
        console.log('Archivo descargado:', fileURL);
        
        // Establece la URL para ReactReader
        setEpubUrl(fileURL);

      } catch (error) {
        console.error('Error fetching data:', error);
      }
    };

    fetchData();
    
    // Cleanup: liberar el objeto URL cuando el componente se desmonte
    return () => {
      if (epubUrl) {
        URL.revokeObjectURL(epubUrl);
      }
    };
  }, [id, location.search]);

  return (
    <div style={{ height: '100vh' }}>
      {epubUrl ? (
        <ReactReader
          url={epubUrl}
          location={locationState}
          onLocationChanged={(epubcfi) => setLocationState(epubcfi)}
          epubInitOptions={{
            openAs: 'epub',
          }}
        />
      ) : (
        <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100%' }}>
          Cargando libro...
        </div>
      )}
    </div>
  )
}

export default Visor