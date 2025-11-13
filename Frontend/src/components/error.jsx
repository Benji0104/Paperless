const MensajeError = ({ tituloM, mensaje }) => {
    return (
        <>
            <div className="col-12 text-center">
              <div className="alert alert-info">
                <h5>{tituloM}</h5>
                <p className="mb-0">
                  {mensaje}
                </p>
              </div>
            </div>
        </>
        )
    }
    export default MensajeError;