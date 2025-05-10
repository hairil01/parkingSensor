import React, { useEffect, useState } from "react";
import "./App.css";

function SensorCard({ name, distance, occupied }) {
  return (
    <div className="card">
      <h2>{name}</h2>
      <div className="distance">Distance: {distance}</div>
      <div className={`status ${occupied ? "occupied" : "not-occupied"}`}>
        {occupied ? "🚗 Parking Occupied" : "🅿️ Not Occupied"}
      </div>
    </div>
  );
}

function App() {
  const [data, setData] = useState({
    sensor1: { distance: "Loading...", occupied: false },
    sensor2: { distance: "Loading...", occupied: false },
  });

  useEffect(() => {
    const fetchData = () => {
      fetch("http://localhost:5000/api/data")
        console.log(data)
        .then((res) => res.json())
        .then((json) => setData(json))
        .catch((err) => console.error("Error fetching:", err));
    };

    fetchData();
    const interval = setInterval(fetchData, 2000); // Poll every 2 sec

    return () => clearInterval(interval); // cleanup
  }, []);

  return (
    <div className="App">
      <h1>Smart Parking Sensors</h1>
      <div className="container">
        <SensorCard name="Sensor 1" {...data.sensor1} />
        <SensorCard name="Sensor 2" {...data.sensor2} />
      </div>
    </div>
  );
}

export default App;
