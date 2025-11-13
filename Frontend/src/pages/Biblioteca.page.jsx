import { useEffect, useState } from "react";
import MensajeCargando from "../components/cargar.jsx";
import MensajeError from "../components/error.jsx";
import "../styles/Biblioteca.css";
import { Docs } from "../hooks/docs";

const MiBiblioteca = () => {
  const { lista } = Docs();
  const [archivos, setArchivos] = useState([]);
  const [cargando, setCargando] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const obtenerArchivos = async () => {
      try {
        setCargando(true);
        setError(null);
        const res = await lista();
        const archivosData = res.archivos || [];
        
        if (archivosData.length > 0) {
         
        }

        // Mapear las propiedades CORRECTAMENTE
        const archivosFormateados = archivosData.map(archivo => ({
          id: archivo.id,
          nombre: archivo.name, //name' del backend
          url: archivo.webViewLink, //'webViewLink' del backend  
          picture: archivo.thumbnailLink || '/documento.svg', //'thumbnailLink'
          visto: archivo.viewedByMeTime,// 'modifiedTime'
          type_doc: archivo.mimeType
        }));

        

        setArchivos(archivosFormateados);
        
      } catch (err) {

        setError("Error al cargar los archivos. Por favor, intenta nuevamente.");
      } finally {
        setCargando(false);
      }
    };

    obtenerArchivos();
  }, []);

  if (cargando) {
    return (
      <MensajeCargando mensaje="Cargando tu biblioteca..." />
    );
  }

  if (error) {
    return (
      <div className="container mt-5">
        <h1 className="text-center">Mi Biblioteca</h1>
        <div className="alert alert-danger text-center" role="alert">
          {error}
        </div>
      </div>
    );
  }

  return (
    <>
      <div className="container mt-5">
        <h1 className="text-center">Mi Biblioteca</h1>
        {archivos.length > 0 && (
          <p className="text-center text-muted">
            Se encontraron {archivos.length} archivos PDF
          </p>
        )}
      </div>

      <div className="container mt-4">
        <div className="row">
          {archivos.length > 0 ? (
            archivos.map((archivo, index) => (
              <div className="col-md-4 mb-4" key={archivo.id || index}>
                <div className="card h-100 shadow-sm">
                  <img
                    src={archivo.picture}
                    className="card-img-top"
                    alt={archivo.nombre}
                    style={{ 
                      height: "200px", 
                      objectFit: "cover",
                      backgroundColor: "#f8f9fa" 
                    }}
                    onError={(e) => {
                      // Si falla la imagen de Google, usar una por defecto
                      e.target.src = '/documentos';
                      e.target.alt = 'Miniatura no disponible';
                    }}
                  />
                  <div className="card-body d-flex flex-column">
                    <h6 className="card-title" style={{ 
                      overflow: 'hidden', 
                      textOverflow: 'ellipsis', 
                      whiteSpace: 'nowrap',
                      minHeight: '1.5rem'
                    }}>
                      {archivo.nombre}
                    </h6>
                     <p className="card-text small text-muted flex-grow-1">
                      ultima ves visto: {archivo.visto}
                    </p>
                    <a 
                      href={`/visor/${archivo.id}`} //{archivo.type_doc !== 'application/pdf' ? `/visor/${archivo.id}` : `/visor/${archivo.id}`}
                      className="btn btn-primary btn-sm mt-auto"
                      target="_blank" 
                    >
                      leer documento
                    </a>
                  </div>
                </div>
              </div>
            ))
          ) : (

            <MensajeError 
              tituloM="Biblioteca Vacía" 
              mensaje="No se encontraron archivos en tu biblioteca. Sube algunos documentos para empezar a leer." 
            />
          )}
        </div>
      </div>
    </>
  );
};

export default MiBiblioteca;



