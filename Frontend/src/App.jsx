import Navbar from './components/Navbar';
import MiBiblioteca from './pages/Biblioteca.page';
import Login from './pages/Login.page';
import Inicio from './pages/Inicio.page';
import Validacion from './pages/Recarga.registro.jsx';
import Conversor from './pages/conversor.page.jsx';
import Visor from './pages/visor.page.jsx';
import VisorPdf from './pages/visorPdf.Page.jsx';
import Perfil from './pages/perfil.page.jsx';
import { Route, Routes, useLocation } from 'react-router-dom';

function App() {
  const location = useLocation();
  const hideNavbarRoutes = ['/', '/login']; // rutas donde no quieres mostrar el navbar
  const shouldHideNavbar = hideNavbarRoutes.includes(location.pathname);

  return (
    <>
      {!shouldHideNavbar && <Navbar />}

      <Routes>
        <Route path="/" element={<Login />} />
        <Route path="/perfil" element={<Perfil />} />
        <Route path="/login" element={<Login />} />
        <Route path="/biblioteca" element={<MiBiblioteca />} />
        <Route path="/inicio" element={<Inicio />} />
        <Route path="/validar" element={<Validacion />} />
        <Route path="/conversor" element={<Conversor />} /> 
        {/* Soportar parámetro de ruta: /visor/123 */}
        <Route path="/visor/:id" element={<Visor />} />
        <Route path="/visorPdf" element={<VisorPdf />} />
        <Route path ="*" >ERROR</Route>
      </Routes>
    </>
  );
}

export default App;

 