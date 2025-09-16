// Arquivo: src/frontend/src/components/RecentOrdersTable.jsx
import React, { useState, useEffect } from 'react';

const RecentOrdersTable = () => {
  const [orders, setOrders] = useState([]);

  useEffect(() => {
    const fetchRecentOrders = async () => {
      const response = await fetch('http://127.0.0.1:8000/api/orders/recent');
      const data = await response.json();
      setOrders(data);
    };
    fetchRecentOrders();
  }, []);

  return (
    <div className="chart-container">
      <h3>Pedidos Recentes</h3>
      <table className="recent-orders-table">
        <thead>
          <tr>
            <th>Cliente</th>
            <th>Valor</th>
            <th>Status</th>
          </tr>
        </thead>
        <tbody>
          {orders.map(order => (
            <tr key={order.orderId}>
              <td>{order.customer_name}</td>
              <td>R$ {order.value.toFixed(2)}</td>
              <td>
                <span className={`status-badge ${order.status === 'CONCLUDED' ? 'status-concluded' : 'status-canceled'}`}>
                  {order.status === 'CONCLUDED' ? 'Concluído' : 'Cancelado'}
                </span>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default RecentOrdersTable;