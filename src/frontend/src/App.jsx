// Arquivo: src/frontend/src/App.jsx
import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Sidebar from '/src/components/Sidebar.jsx';
import VisaoGeral from './pages/VisaoGeral';
import './App.css';

// Páginas de exemplo para o futuro
const VendasPage = () => <div className="page-content"><h1>Análise de Vendas (Em construção)</h1></div>;
const ClientesPage = () => <div className="page-content"><h1>Análise de Clientes (Em construção)</h1></div>;

function App() {
  return (
    <Router>
      <div className="dashboard-layout">
        <Sidebar />
        <main className="main-content">
          <Routes>
            <Route path="/" element={<VisaoGeral />} />
            <Route path="/vendas" element={<VendasPage />} />
            <Route path="/clientes" element={<ClientesPage />} />
          </Routes>
        </main>
      </div>
    </Router>
  );
}

export default App;