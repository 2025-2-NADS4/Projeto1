// Arquivo: src/frontend/src/components/SalesChannelChart.jsx

import React, { useState, useEffect } from 'react';
import { Pie } from 'react-chartjs-2';
import { Chart as ChartJS, ArcElement, Tooltip, Legend } from 'chart.js';

// Registra os componentes necessários do Chart.js
ChartJS.register(ArcElement, Tooltip, Legend);

const SalesChannelChart = () => {
  const [chartData, setChartData] = useState(null);
  const [error, setError] = useState('');

  useEffect(() => {
    const fetchChartData = async () => {
      try {
        // Chama o nosso novo endpoint no back-end
        const response = await fetch('http://127.0.0.1:8000/api/performance/by_sales_channel');
        if (!response.ok) {
          throw new Error('Resposta da rede não foi boa!');
        }
        const data = await response.json();

        // Formata os dados para o formato que o Chart.js espera
        const formattedData = {
          labels: Object.keys(data), // Ex: ['IFOOD', 'EPADOCA', 'ANOTAAI']
          datasets: [
            {
              label: 'Receita por Canal',
              data: Object.values(data), // Ex: [50000.0, 34500.50, 25000.75]
              backgroundColor: [
                'rgba(255, 99, 132, 0.7)',
                'rgba(54, 162, 235, 0.7)',
                'rgba(255, 206, 86, 0.7)',
                'rgba(75, 192, 192, 0.7)',
                'rgba(153, 102, 255, 0.7)',
              ],
              borderColor: [
                'rgba(255, 99, 132, 1)',
                'rgba(54, 162, 235, 1)',
                'rgba(255, 206, 86, 1)',
                'rgba(75, 192, 192, 1)',
                'rgba(153, 102, 255, 1)',
              ],
              borderWidth: 1,
            },
          ],
        };
        setChartData(formattedData);
      } catch (error) {
        console.error("Falha ao buscar dados para o gráfico:", error);
        setError("Não foi possível carregar os dados do gráfico.");
      }
    };

    fetchChartData();
  }, []);

  if (error) {
    return <div className="chart-container"><p style={{ color: 'red' }}>{error}</p></div>;
  }

  if (!chartData) {
    return <div className="chart-container"><p>Carregando gráfico...</p></div>;
  }

  return (
    <div className="chart-container">
      <h3>Receita por Canal de Venda</h3>
      <Pie data={chartData} />
    </div>
  );
};

export default SalesChannelChart;