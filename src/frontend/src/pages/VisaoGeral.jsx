// Arquivo: src/frontend/src/pages/VisaoGeral.jsx (versão com layout refinado)
import React, { useState, useEffect } from 'react';
import SalesChannelChart from '../components/SalesChannelChart';
import RevenueChart from '../components/RevenueChart';
import RecentOrdersTable from '../components/RecentOrdersTable';

const VisaoGeral = () => {
  const [kpis, setKpis] = useState(null);
  const [error, setError] = useState('');

  useEffect(() => {
    // ... (a lógica de fetchKpis continua a mesma)
    const fetchKpis = async () => {
      try {
        const response = await fetch('http://127.0.0.1:8000/api/kpis/gerais');
        if (!response.ok) throw new Error('A resposta da rede não foi boa!');
        const data = await response.json();
        setKpis(data);
      } catch (error) {
        setError("Não foi possível carregar os KPIs.");
      }
    };
    fetchKpis();
  }, []);

  return (
    <div className="page-content">
      <h1>Visão Geral</h1>
      
      {/* Container dos KPIs (agora fora do grid para ficar sempre no topo) */}
      <div className="kpi-container">
        {error && <p style={{ color: 'red' }}>{error}</p>}
        {!kpis && !error && <p>Carregando KPIs...</p>}
        {kpis && (
          <div className="kpis">
            <div className="kpi-card"><h3>Receita Total</h3><p>R$ {kpis.total_revenue}</p></div>
            <div className="kpi-card"><h3>Total de Pedidos</h3><p>{kpis.total_orders}</p></div>
            <div className="kpi-card"><h3>Ticket Médio</h3><p>R$ {kpis.average_ticket}</p></div>
            <div className="kpi-card"><h3>Novos Clientes (30d)</h3><p>{kpis.new_customers_last_30d}</p></div>
            <div className="kpi-card"><h3>Taxa de Cancelamento</h3><p>{kpis.cancellation_rate}%</p></div>
          </div>
        )}
      </div>

      {/* Grid para os gráficos e tabelas */}
      <div className="dashboard-grid">
        {/* Este item ocupa a largura total */}
        <div className="grid-item-full">
          <RevenueChart />
        </div>
        
        {/* Estes dois itens ocuparão uma coluna cada, ficando lado a lado */}
        <SalesChannelChart />
        <RecentOrdersTable />
      </div>
    </div>
  );
};

export default VisaoGeral;