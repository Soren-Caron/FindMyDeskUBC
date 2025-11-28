import { useState, useEffect } from "react";
import { spots } from "../../data/spots";

export default function Sidebar({ onSelectSpot, onFilteredChange }) {
  const [activeFilters, setActiveFilters] = useState([]);
  const [search, setSearch] = useState("");

  const filters = [
    { id: "quiet", label: "Quiet" },
    { id: "group", label: "Group Friendly" },
    { id: "outlets", label: "Power Outlets" },
    { id: "food", label: "Food Nearby" },
  ];

  const toggleFilter = (filterId) => {
    setActiveFilters((prev) =>
      prev.includes(filterId)
        ? prev.filter((f) => f !== filterId)
        : [...prev, filterId]
    );
  };

  const filteredSpots = spots.filter((spot) => {
    const matchesSearch = spot.name.toLowerCase().includes(search.toLowerCase());
    const matchesFilters =
      activeFilters.length === 0 ||
      activeFilters.every((f) => spot.features?.includes(f));
    return matchesSearch && matchesFilters;
  });

  useEffect(() => {
    onFilteredChange(filteredSpots);
  }, [activeFilters, search]);

  return (
    <div
      style={{
        width: "280px",
        background: "#1e1e1e",
        color: "white",
        padding: "20px",
        boxSizing: "border-box",  // ⭐ FIX
        overflowY: "auto",
        overflowX: "hidden",      // ⭐ FIX
        boxShadow: "-2px 0 8px rgba(0,0,0,0.4)",
        display: "flex",
        flexDirection: "column",
        height: "100%",
      }}
    >
      <h2 style={{ marginTop: 0 }}>Study Spots</h2>

      {/* Search Bar */}
      <input
        type="text"
        placeholder="Search spots..."
        value={search}
        onChange={(e) => setSearch(e.target.value)}
        style={{
          width: "100%",
          padding: "10px",
          borderRadius: "8px",
          border: "none",
          marginBottom: "15px",
          background: "#2c2c2c",
          color: "white",
        }}
      />

      {/* Spots List */}
      <div style={{ flex: 1 }}>
        {filteredSpots.map((spot) => (
          <div
            key={spot.id}
            onClick={() => onSelectSpot(spot)}
            style={{
              padding: "12px",
              marginBottom: "10px",
              background: "#2c2c2c",
              borderRadius: "10px",
              cursor: "pointer",
              transition: "0.2s",
            }}
            onMouseEnter={(e) => (e.currentTarget.style.background = "#3a3a3a")}
            onMouseLeave={(e) => (e.currentTarget.style.background = "#2c2c2c")}
          >
            <strong>{spot.name}</strong>
            <br />
            <small>Click to view on map</small>
          </div>
        ))}
        {filteredSpots.length === 0 && (
          <p style={{ opacity: 0.6 }}>No spots match your filters/search.</p>
        )}
      </div>

      {/* Filters */}
      <div
        style={{
          marginTop: "20px",
          padding: "10px",
          background: "#2a2a2a",
          borderRadius: "10px",
        }}
      >
        <h3 style={{ margin: 0, marginBottom: "10px" }}>Filters</h3>

        <div style={{ display: "flex", flexWrap: "wrap", gap: "8px" }}>
          {filters.map((f) => (
            <button
              key={f.id}
              onClick={() => toggleFilter(f.id)}
              style={{
                padding: "6px 10px",
                borderRadius: "8px",
                border: "none",
                cursor: "pointer",
                background: activeFilters.includes(f.id)
                  ? "#4caf50"
                  : "#3a3a3a",
                color: "white",
              }}
            >
              {f.label}
            </button>
          ))}
        </div>
      </div>
    </div>
  );
}
