import { useState } from "react";

export default function SubirArchivos() {
  const [archivos, setArchivos] = useState([]);

  const manejarCambio = (e) => {
    setArchivos([...e.target.files]);
  };

  return (
    <div style={{ padding: "20px" }}>
      <h2>Subir Archivos</h2>

      {/* Botón para elegir archivos */}
      <input type="file" multiple onChange={manejarCambio} />

      {/* Lista de archivos seleccionados */}
      <ul>
        {archivos.map((archivo, i) => (
          <li key={i}>{archivo.name}</li>
        ))}
      </ul>
    </div>
  );
}