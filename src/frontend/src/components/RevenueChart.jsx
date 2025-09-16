// Arquivo: src/frontend/src/components/RevenueChart.jsx
import React, { useState, useEffect } from 'react';
import { Line } from 'react-chartjs-2';
import { Chart as ChartJS, CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend } from 'chart.js';

ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend);

const RevenueChart = () => {
  const [chartData, setChartData] = useState(null);

  useEffect(() => {
    const fetchChartData = async () => {
      const response = await fetch('http://127.0.0.1:8000/api/performance/revenue_last_7_days');
      const data = await response.json();

      setChartData({
        labels: Object.keys(data),
        datasets: [{
          label: 'Receita (R$)',
          data: Object.values(data),
          fill: false,
          borderColor: 'var(--color-primary)',
          tension: 0.1
        }]
      });
    };
    fetchChartData();
  }, []);

  if (!chartData) return <div className="chart-container"><p>Carregando gráfico...</p></div>;

  return (
    <div className="chart-container">
      <h3>Receita (Últimos 7 dias)</h3>
      <Line data={chartData} />
    </div>
  );
};

export default RevenueChart;