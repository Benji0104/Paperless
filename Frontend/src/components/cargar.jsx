const MensajeCarga = ({ mensaje = "Cargando..." }) => {
    return (
        <>
            <div className="container mt-5">
                <h1 className="text-center">{mensaje}</h1>
                <div className="d-flex justify-content-center align-items-center" style={{ height: "50vh" }}>
                    <div className="text-center">
                        <div className="spinner-border text-primary" style={{ width: "3rem", height: "3rem" }} role="status">
                            <span className="visually-hidden">Cargando...</span>
                        </div>
                        <p className="mt-3">{mensaje}</p>
                    </div>
                </div>
            </div>
        </>
    );
};



export default MensajeCarga;