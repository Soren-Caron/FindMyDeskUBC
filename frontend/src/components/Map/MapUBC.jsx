/**
 * Displays an interactive map of UBC with:
 *   - markers for study spots
 *   - a heatmap based on how busy each spot is
 *   - recentring on a selected spot
 *
 * This is the main map component used in the frontend to show
 * where each spot is on campus and how busy it is.
 */

// ------------------- IMPORTS -------------------
import { MapContainer, TileLayer, Marker, Popup, useMap } from "react-leaflet";
import "leaflet/dist/leaflet.css";

import L from "leaflet";

// Fix Vite marker icon issue
import iconUrl from "leaflet/dist/images/marker-icon.png";
import iconRetinaUrl from "leaflet/dist/images/marker-icon-2x.png";
import shadowUrl from "leaflet/dist/images/marker-shadow.png";

// Required so Leaflet loads icons correctly in Vite
delete L.Icon.Default.prototype._getIconUrl;

L.Icon.Default.mergeOptions({
  iconUrl,
  iconRetinaUrl,
  shadowUrl,
});

import { spots } from "../../data/spots";
import HeatmapLayer from "./HeatmapLayer";
// ------------------- RECENTER COMPONENT -------------------
/**
 * Purpose:
 *   Recenters the map when the user selects a specific study spot.
 *
 * Inputs:
 *   selectedSpot:
 *     Object containing { lat, lng }. The map view shifts
 *     to this location with a smooth animation. If null, nothing happens.
 *
 * Output:
 *   Returns null. This function does not display UI.
 */

function RecenterOnSpot({ selectedSpot }) {
  const map = useMap();
  if (selectedSpot) {
    map.setView([selectedSpot.lat, selectedSpot.lng], 17, { animate: true });
  }
  return null;
}
// --------------------- MAIN MAP --------------------------
/**
 * Purpose:
 *   Main map for showing UBC study spots. Displays markers and a heatmap
 *   based on each spot's busy_score. Also recenters the map if a spot is selected.
 *
 * Inputs:
 *   selectedSpot:
 *     The spot the user clicked on. If set, the map moves to this location.
 *
 *   filteredSpots:
 *     Optional list of spots to show. If not given or empty, show all spots.
 *
 * Output:
 *   Returns the full Leaflet map with markers, popups, the heatmap, and recentering.
 */

export default function MapUBC({ selectedSpot, filteredSpots }) {
  const spotsToShow =
    filteredSpots && filteredSpots.length > 0 ? filteredSpots : spots;

  // ---- Normalize + Clamp + Boost for heatmap ----
  let heatmapPoints = [];
  if (spotsToShow.length > 0) {
    const scores = spotsToShow.map((s) => s.busy_score ?? 0.5);
    const min = Math.min(...scores);
    const max = Math.max(...scores);
    const range = max - min || 1;

    heatmapPoints = spotsToShow.map((s) => {
      const raw = s.busy_score ?? 0.5;

      let normalized = (raw - min) / range; // normalize 0–1
      normalized = Math.max(normalized, 0.25); // clamp low intensities
      normalized = Math.pow(normalized, 0.75); // boost high intensities

      return [s.lat, s.lng, normalized];
    });
  }

  // --------------------- RENDER MAP ----------------------
  return (
    <div
      style={{
        height: "100%",
        width: "100%",
        position: "absolute",
        inset: 0,
      }}
    >
      <MapContainer
        center={[49.2665, -123.25]}
        zoom={15}
        scrollWheelZoom={true}
        style={{ height: "100%", width: "100%" }}
      >
        <TileLayer url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png" />

        {/* Recenter map to selected spot */}
        <RecenterOnSpot selectedSpot={selectedSpot} />

        {/* Heatmap */}
        <HeatmapLayer points={heatmapPoints} />

        {/* Map Markers */}
        {spotsToShow.map((spot) => (
          <Marker key={spot.id} position={[spot.lat, spot.lng]}>
            <Popup>
              <strong>{spot.name}</strong>
              <br />
              Busy Score: {spot.busy_score}
            </Popup>
          </Marker>
        ))}
      </MapContainer>
    </div>
  );
}
