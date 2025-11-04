import '../styles/Inicio.css';

const Inicio = () => {
  return (
    <>
      <header className="inicio">
        <div className="overlay">
          <div className="container text-center text-light">
            <div className="inicio-subheading">Bienvenido a PAPERLESS</div>
            <div className="inicio-heading text-uppercase">Tu biblioteca digital</div>
          </div>
        </div>
      </header>

      <section className="page-section" id="info">
        <div className="container">
          <div className="text-center mb-5">
            <h2 className="section-heading text-uppercase">¿Quiénes somos?</h2>
            <h3 className="section-subheading text-muted">Nuestra misión, visión y propósito</h3>
          </div>
          <div className="row text-center">
            <div className="col-md-4">
              <h4 className="my-3">Misión</h4>
              <p className="text-muted">
                Facilitar el acceso, organización y conversión de documentos digitales para estudiantes, profesionales y curiosos del conocimiento.
              </p>
            </div>
            <div className="col-md-4">
              <h4 className="my-3">Visión</h4>
              <p className="text-muted">
                Ser la plataforma líder en gestión documental digital, promoviendo el aprendizaje sin papel y la eficiencia en el manejo de información.
              </p>
            </div>
            <div className="col-md-4">
              <h4 className="my-3">Acerca de</h4>
              <p className="text-muted">
                PAPERLESS es una aplicación web pensada para ayudarte a convertir, almacenar y explorar tus documentos de forma rápida y segura.
              </p>
            </div>
          </div>
        </div>
      </section>
    </>
  );
};

export default Inicio;