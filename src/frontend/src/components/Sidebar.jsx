// Arquivo: src/frontend/src/components/Sidebar.jsx
import React from 'react';
import { Link } from 'react-router-dom';
import './Sidebar.css'; // Criaremos este CSS em breve

const Sidebar = () => {
  return (
    <div className="sidebar">
      <div className="sidebar-header">
        <h2>Cannoli BI</h2>
      </div>
      <nav className="sidebar-nav">
        <ul>
          {/* O 'Link to="/"' nos levará para a página inicial */}
          <li><Link to="/">Visão Geral</Link></li>
          {/* No futuro, adicionaremos mais links aqui */}
          <li><Link to="/vendas">Análise de Vendas</Link></li>
          <li><Link to="/clientes">Análise de Clientes</Link></li>
        </ul>
      </nav>
    </div>
  );
};

export default Sidebar;