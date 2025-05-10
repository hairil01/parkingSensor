import React from 'react';

export default function SensorCard({ title, data }) {
  return (
    <div className="card">
      <h2>{title}</h2>
      <p>Distance: {data.distance}</p>
      <div className={`status ${data.occupied ? 'occupied' : 'free'}`}>
        {data.occupied ? '🚗 Parking Occupied' : '🅿️ Not Occupied'}
      </div>
    </div>
  );
}
