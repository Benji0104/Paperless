import Navbar from './components/Navbar';
import MiBiblioteca from './pages/Biblioteca.page';
import Login from './pages/Login.page';
import Inicio from './pages/Inicio.page';
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
        <Route path="/login" element={<Login />} />
        <Route path="/biblioteca" element={<MiBiblioteca />} />
        <Route path="/inicio" element={<Inicio />} />
      </Routes>
    </>
  );
}

export default App;

 