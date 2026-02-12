import logo from './logo.svg';
import './App.css';
import { BrowserRouter, Routes, Route } from "react-router-dom";
import { useState } from 'react';

import "./styles/comun.css";

import Nav from './componentes/Menu/public/Nav';
import Footer from './componentes/Footer/Footer';

import Inicio from './pages/public/Inicio';
import Acceso from './pages/public/Acceso';
import ComoFunciona from './pages/public/ComoFunciona';
import Curiosidades from './pages/public/Curiosidades';
import SobreNosotros from './pages/public/SobreNosotros';
import Contacto from './pages/public/Contacto';
import PublicLayout from './layouts/PublicLayout';
import LayoutApp from './layouts/LayoutApp';


function App() {

  return (
    <BrowserRouter>
      <Routes>

        <Route element={<LayoutApp />}>

          <Route element={<PublicLayout />}>
            <Route path="/" element={<Inicio />} />
            <Route path="/sobre-nosotros" element={<SobreNosotros />} />
            <Route path="/como-funciona" element={<ComoFunciona />} />
            <Route path="/contacto" element={<Contacto />} />
            <Route path="/acceso" element={<Acceso />} />
          </Route>

        </Route>

      </Routes>
        {/*menu privado mas adelante junto a back
        <Route path="/rueda-emociones" element={<Calendario />} />
        <Route path="/estadisticas" element={<Estadisticas />} />
        <Route path="/recomendaciones" element={<Recomendaciones />} />
        <Route path="/logros" element={<Logros />} />*/}

    </BrowserRouter>
  );
}

export default App;
