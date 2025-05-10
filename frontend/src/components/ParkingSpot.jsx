// src/components/ParkingSpot.jsx
import React from 'react';
import carImage from '../assets/car.png';
import './ParkingSpot.css';

const ParkingSpot = ({ name, distance, occupied }) => {
  return (
    <div className="parking-card">
      <h2>{name}</h2>
      <div className="distance">Distance: {distance}</div>
      <div className={`spot ${occupied ? 'occupied' : 'free'}`}>
        {occupied && <img src={carImage} alt="Car" className="car-img" />}
      </div>
      <div className={`status ${occupied ? 'red' : 'green'}`}>
        {occupied ? '🚗 Occupied' : '🅿️ Available'}
      </div>
    </div>
  );
};

export default ParkingSpot;
