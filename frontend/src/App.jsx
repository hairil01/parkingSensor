import React, { useEffect, useState } from 'react';
import ParkingSpot from './components/ParkingSpot';
import './App.css';

function App() {
  const [data, setData] = useState({
    sensor1: { distance: 'Loading...', occupied: false },
    sensor2: { distance: 'Loading...', occupied: false },
  });

  useEffect(() => {
    const fetchData = () => {
      fetch('http://192.168.100.13:5000/api/sensors')
        .then((res) => res.json())
        .then((json) => {
          setData(json);
        })
        .catch((err) => console.error('API error:', err));
    };

    fetchData(); // Initial fetch
    const interval = setInterval(fetchData, 1000); // Refresh every 1 seconds

    return () => clearInterval(interval);
  }, [data]);

  return (
    <div className="App">
      <h1>🚗 Smart Parking Lot</h1>
      <div className="parking-container">
        <ParkingSpot
          name="Parking 1"
          distance={data.sensor1.distance}
          occupied={data.sensor1.occupied}
        />
        <ParkingSpot
          name="Parking 2"
          distance={data.sensor2.distance}
          occupied={data.sensor2.occupied}
        />
      </div>
    </div>
  );
}

export default App;
