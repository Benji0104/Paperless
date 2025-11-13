import { useState } from "react";
import { useAuth } from '../hooks/useAuth';
import '../styles/conversor.css'

const Conversor = () => {
  const [files, setFiles] = useState([]);
  const [converted, setConverted] = useState([]);
  const [loading, setLoading] = useState(false);
  const {convertFiles } = useAuth();

  const handleFileChange = (e) => {
    const newFiles = Array.from(e.target.files);
    setFiles(newFiles);
  };
    
 const uploadFiles = async () => {
  if (files.length === 0) {
    alert("Selecciona al menos un archivo PDF");
    return;
  }
  setLoading(true);
  try {
    const result = await convertFiles(files);
    console.log('Resultados de la conversión:', result); // DEBUG
    setConverted(result);
  } catch (err) {
    console.error(err);
  } finally {
    setLoading(false);
  }
};

  return (
    <div className="container mt-4" style={{ maxWidth: "500px" }}>
      <div className="card shadow-sm border-0">
        <div className="card-body">
          <h5 className="card-title fw-semibold">Convertir PDF a EPUB</h5>
          <p className="text-muted small mb-3">
            Sube uno o varios archivos PDF para convertirlos
          </p>

          {/* Zona de carga */}
          <label
            htmlFor="file-upload"
            className="d-flex flex-column align-items-center justify-content-center border border-2 border-secondary rounded-3 py-5 text-center bg-light"
            style={{ cursor: "pointer", borderStyle: "dashed" }}
          >
            <i className="bi bi-cloud-arrow-up fs-1 text-secondary mb-2"></i>
            <p className="mb-0 fw-semibold">Selecciona archivos PDF</p>
            <small className="text-muted">Solo formato PDF</small>
            <input
              id="file-upload"
              type="file"
              accept=".pdf"
              multiple
              className="d-none"
              onChange={handleFileChange}
            />
          </label>

          {/* Botón de subir */}
          <div className="text-center mt-3">
            <button
              onClick={uploadFiles}
              className="btn btn-primary"
              disabled={loading}
            >
              {loading ? "Convirtiendo..." : "Convertir a EPUB"}
            </button>
          </div>
    
          {loading ? <div className="loader"></div>:null}

          {/* Mostrar archivos seleccionados */}
          <div className="mt-3">
            {files.map((file, i) => (
              <div
                key={i}
                className="d-flex align-items-center justify-content-between border rounded px-3 py-2 mb-2 bg-white"
              >
                <div className="d-flex align-items-center gap-2">
                  <i className="bi bi-file-earmark-pdf text-danger fs-5"></i>
                  <span className="small">{file.name}</span>
                </div>
              </div>
            ))}
          </div>

          <hr />

          {/* Aquí se muestran los archivos convertidos */}
          <div>
            <h6 className="fw-semibold">Archivos convertidos:</h6>
            {converted.length === 0 && (
              <p className="text-muted small">Aún no hay resultados</p>
            )}

            {converted.map((item, index) => (
              <div
                key={index}
                className="border rounded p-2 mb-2 bg-white small"
              >
                <div className="fw-semibold text-primary">
                  {item.archivo_pdf}
                </div>

                {item.error ? (
                  <div className="text-danger">
                    ❌ Error: {item.error}
                  </div>
                ) : (
                  <div className="text-success">
                    ✅ Convertido correctamente
                    <div>
                      <a
                      
                      className="btn btn-sm btn-outline-success mt-1"
                      href={item.epub_path}
                      download>


                      </a>
                      
                    </div>
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};

export default Conversor;
