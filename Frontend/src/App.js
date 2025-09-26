import logo from './logo.svg';
import './App.css';
import Component from './Component';
import SubirArchivos from './SubirArchivos';

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        <p>
          Hola react.
        </p>
        <a
          className="App-link"
          href="https://reactjs.org"
          target="_blank"
          rel="noopener noreferrer"
        >
          Learn React
        </a>
        
        <Component />
        <SubirArchivos />
      
      </header>
    </div>
  );
}

export default App;
