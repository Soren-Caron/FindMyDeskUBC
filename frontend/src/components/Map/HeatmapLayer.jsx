import { useMap } from "react-leaflet";
import "leaflet.heat";
import { useEffect } from "react";

export default function HeatmapLayer({ points }) {
  const map = useMap();

  useEffect(() => {
    if (!map || !points || points.length === 0) return;

    const heat = window.L.heatLayer(points, {
      radius: 65,         
      blur: 15,         
      maxOpacity: 1.0,  
      maxZoom: 19,
      gradient: {
        0.0: "green",
        0.3: "yellowgreen",
        0.5: "yellow",
        0.7: "orange",
        0.9: "red",     
      },
    }).addTo(map);

    return () => heat.remove();
  }, [map, points]);

  return null;
}
