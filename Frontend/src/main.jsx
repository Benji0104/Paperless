// src/main.jsx
import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App.jsx'   // 👈 IMPORTANTE: Asegúrate de tener esta línea
import { BrowserRouter } from 'react-router-dom';
import 'bootstrap/dist/css/bootstrap.min.css'; // estilos
import 'bootstrap/dist/js/bootstrap.bundle.min.js'; // funcionalidad JS (navbar, modales, etc.)
import '@fortawesome/fontawesome-free/css/all.min.css'; // iconos



ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <BrowserRouter>
      <App />   {/* 👈 Aquí usa el componente App */}
    </BrowserRouter>
  </React.StrictMode>,
)