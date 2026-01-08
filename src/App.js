import logo from './logo.svg';
import './App.css';
import { BrowserRouter, Routes, Route } from "react-router-dom";
import { useState } from 'react';

import Nav from './componentes/Menu/Nav';
import Footer from './componentes/Footer/Footer';

import Inicio from './pages/Inicio';
import Acceso from './pages/Acceso';
import ComoFunciona from './pages/ComoFunciona';
import Curiosidades from './pages/Curiosidades';
import SobreNosotros from './pages/SobreNosotros';
import Contacto from './pages/Contacto';

function App() {

  const [logueado, setLogueado] = useState(false)
  return (
    <BrowserRouter>
      <Nav logueado={logueado} />
      <Routes>
        <Route path="/" element={<Inicio />} />
        <Route path="/sobre-nosotros" element={<SobreNosotros />} />
        <Route path="/como-funciona" element={<ComoFunciona />} />
        <Route path="/curiosidades" element={<Curiosidades />} />
        <Route path="/acceso" element={<Acceso setLogueado={setLogueado} />} />
        <Route path="/contacto" element={<Contacto />} />

        {/*<Route path="/rueda-emociones" element={<Calendario />} />
        <Route path="/estadisticas" element={<Estadisticas />} />
        <Route path="/recomendaciones" element={<Recomendaciones />} />
        <Route path="/logros" element={<Logros />} />*/}
      </Routes>
      <Footer />
    </BrowserRouter>
  );
}

export default App;
