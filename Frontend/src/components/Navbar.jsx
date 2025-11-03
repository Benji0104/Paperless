function App() {
  return (
    <>
      {/* Navbar de Bootstrap */}
      <nav className="navbar navbar-expand-lg navbar-dark bg-dark">
        <div className="container-fluid">
          <a className="navbar-brand" href="/inicio">
            <img
              src="/paperless-navbar.png"
              alt="Logo"
              style={{ width: '70px', height: '70px' }}
            />
          </a>
          <button
            className="navbar-toggler"
            type="button"
            data-bs-toggle="collapse"
            data-bs-target="#navbarNav"
          >
            <span className="navbar-toggler-icon"></span>
          </button>
          <div className="collapse navbar-collapse" id="navbarNav">
            <ul className="navbar-nav ms-auto">
              <li className="nav-item">
                <a className="nav-link active" href="/inicio">Inicio</a>
              </li>
              <li className="nav-item">
                <a className="nav-link" href="/biblioteca">Mi Biblioteca</a>
              </li>
              <li className="nav-item">
                <a className="nav-link" href="#">Colecciones</a>
              </li>
              <li className="nav-item">
                <a className="nav-link" href="#">Convertir</a>
              </li>
              <li className="nav-item">
                <a className="nav-link" href="#">Mi nube</a>
              </li>
              <li className="nav-item">
                <a className="nav-link" href="/">Login</a>
              </li>
            </ul>
          </div>
        </div>
      </nav>

    </>
  );
}

export default App;