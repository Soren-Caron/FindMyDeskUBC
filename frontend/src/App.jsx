import { useState, useEffect } from "react";
import "leaflet/dist/leaflet.css";
import MapUBC from "./components/Map/MapUBC";
import Sidebar from "./components/Sidebar/Sidebar";
import FeedbackPanel from "./components/Feedback/FeedBackPanel";
import { spots as initialSpots } from "./data/spots";

export default function App() {
  const [selectedSpot, setSelectedSpot] = useState(null);

  const [spotsData, setSpotsData] = useState([]);
  const [filteredSpots, setFilteredSpots] = useState([]);

  const [clientSessionId] = useState(() => {
    const existing = localStorage.getItem("client_session_id");
    if (existing) return existing;
    const newId = crypto.randomUUID?.() ?? Math.random().toString(36).slice(2);
    localStorage.setItem("client_session_id", newId);
    return newId;
  });

  useEffect(() => {
    async function loadScores() {
      const now = new Date().toISOString();

      const updated = await Promise.all(
        initialSpots.map(async (spot) => {
          try {
            const res = await fetch(
              `http://127.0.0.1:8000/predict?spot=${encodeURIComponent(
                spot.name
              )}&timestamp=${now}`
            );

            if (!res.ok) throw new Error("API error");

            const data = await res.json();

            return {
              ...spot,
              busy_score: data.busy_score ?? 0.5,
            };
          } catch (err) {
            console.warn("Failed to fetch busy score for:", spot.name);
            return { ...spot, busy_score: 0.5 };
          }
        })
      );

      setSpotsData(updated);
      setFilteredSpots(updated);
      console.log("🔥 Loaded busy scores:", updated);
    }

    loadScores();
  }, []);

  return (
    <div style={{ display: "flex", height: "100vh" }}>
      {/* Sidebar */}
      <div style={{ width: 280 }}>
        <Sidebar
          onSelectSpot={setSelectedSpot}
          onFilteredChange={setFilteredSpots}
          spots={spotsData}
        />
      </div>

      {/* Map */}
      <div style={{ flex: 1, position: "relative" }}>
        <MapUBC 
          selectedSpot={selectedSpot}
          filteredSpots={filteredSpots}
        />
      </div>

      <FeedbackPanel 
        selectedSpot={selectedSpot}
        clientSessionId={clientSessionId}
      />
    </div>
  );
}
