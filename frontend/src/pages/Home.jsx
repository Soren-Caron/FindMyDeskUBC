import MapUBC from "../components/Map/MapUBC";

export default function Home() {
  return (
    <div style={{ display: "flex" }}>
      <div style={{ flex: 2 }}>
        <MapUBC />
      </div>

      {/* Placeholder for right-side list */}
      <div style={{ flex: 1, padding: "20px" }}>
        <h2>Top Study Spots</h2>
        <p>List goes here...</p>
      </div>
    </div>
  );
}
