import React, { useState } from "react";

function SubirArchivos() {
  const [archivo, setArchivo] = useState(null);

  const manejarCambio = (e) => {
    setArchivo(e.target.files[0]);
  };

  const manejarSubmit = (e) => {
    e.preventDefault();
    if (archivo) {
      alert(`Archivo seleccionado: ${archivo.name}`);
      // Aquí luego puedes hacer la subida con fetch o axios
    } else {
      alert("Por favor selecciona un archivo antes de enviar.");
    }
  };

  return (
    <div className="container mt-5">
      <div className="card shadow-lg p-4 rounded-3">
        <h3 className="text-center text-primary mb-4">Subir Archivo</h3>

        <form onSubmit={manejarSubmit}>
          {/* Input de archivo con estilo Bootstrap */}
          <div className="mb-3">
            <label htmlFor="formFile" className="form-label fw-bold">
              Selecciona un archivo:
            </label>
            <input
              className="form-control"
              type="file"
              id="formFile"
              onChange={manejarCambio}
            />
          </div>

          {/* Botón de subir */}
          <div className="d-grid">
            <button type="submit" className="btn btn-success">
              Subir archivo
            </button>
          </div>
        </form>

        {/* Mostrar archivo seleccionado */}
        {archivo && (
          <div className="alert alert-info mt-3">
            Archivo seleccionado: <strong>{archivo.name}</strong>
          </div>
        )}
      </div>
    </div>
  );
}

export default SubirArchivos;