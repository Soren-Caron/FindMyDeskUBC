import { useState } from "react";
/**
 * Purpose:
 *   Filter panel for the map. Lets the user toggle openNow, aiOnly, and type.
 *   The panel can also collapse so it doesn't cover the map.
 *
 * Inputs:
 *   filters:
 *     Current filter values coming from the parent component.
 *
 *   setFilters:
 *     Updates the parent's filters whenever the user changes something.
 *
 * Output:
 *   Returns the UI for the panel (checkboxes + dropdown).
 */

export default function FilterPanel({ filters, setFilters }) {
  const [open, setOpen] = useState(true);

  return (
    <div
      style={{
        position: "absolute",
        bottom: open ? "20px" : "-140px",
        left: "20px",
        width: "260px",
        background: "rgba(30,30,30,0.95)",
        padding: "16px",
        borderRadius: "12px",
        color: "white",
        boxShadow: "0px 4px 12px rgba(0,0,0,0.4)",
        transition: "bottom 0.35s ease",
        zIndex: 9999,
      }}
    >
      {/* Collapse Button */}
      <div
        onClick={() => setOpen(!open)}
        style={{
          position: "absolute",
          top: "-32px",
          left: "0",
          width: "120px",
          padding: "6px 10px",
          background: "#1f1f1f",
          borderRadius: "8px 8px 0 0",
          cursor: "pointer",
          textAlign: "center",
          border: "1px solid #333",
        }}
      >
        {open ? "Hide Filters ▼" : "Filters ▲"}
      </div>

      {/* Filters */}
      <h3 style={{ marginTop: 0 }}>Filters</h3>

      {/* Open Now */}
      <label style={{ display: "block", marginBottom: "10px" }}>
        <input
          type="checkbox"
          checked={filters.openNow}
          onChange={(e) =>
            setFilters({ ...filters, openNow: e.target.checked })
          }
        />
        <span style={{ marginLeft: "8px" }}>Open Now</span>
      </label>

      {/* AI Recommended Only */}
      <label style={{ display: "block", marginBottom: "10px" }}>
        <input
          type="checkbox"
          checked={filters.aiOnly}
          onChange={(e) =>
            setFilters({ ...filters, aiOnly: e.target.checked })
          }
        />
        <span style={{ marginLeft: "8px" }}>AI Recommended Only</span>
      </label>

      {/* Indoor / Outdoor */}
      <label style={{ display: "block", marginBottom: "10px" }}>
        <select
          value={filters.type}
          onChange={(e) =>
            setFilters({ ...filters, type: e.target.value })
          }
          style={{
            width: "100%",
            padding: "6px",
            background: "#2c2c2c",
            color: "white",
            borderRadius: "6px",
          }}
        >
          <option value="all">All Types</option>
          <option value="indoor">Indoor</option>
          <option value="outdoor">Outdoor</option>
        </select>
      </label>
    </div>
  );
}
