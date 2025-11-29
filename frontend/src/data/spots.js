/*
Spec (spots.js):

- Exports a static list of study spots on UBC campus.
- Each spot includes:
    id            - unique identifier
    name          - library/space name
    lat, lng      - map coordinates
    features      - simple tags describing the space
    busy_score    - filled later by API; defaults to null
*/
export const spots = [
  { id: 1, name: "IKBLC", lat: 49.267938, lng: -123.252398, features: ["quiet", "outlets"], busy_score: null },

  { id: 2, name: "Koerner", lat: 49.268412, lng: -123.254246, features: ["quiet", "outlets"], busy_score: null },

  { id: 3, name: "David Lam", lat: 49.264581, lng: -123.253088, features: ["quiet", "outlets"], busy_score: null },

  { id: 4, name: "Education", lat: 49.2661, lng: -123.2499, features: ["quiet", "outlets"], busy_score: null },

  { id: 5, name: "Woodward", lat: 49.262853, lng: -123.244119, features: ["quiet", "outlets"], busy_score: null },

  { id: 6, name: "Law", lat: 49.264216, lng: -123.255546, features: ["quiet", "outlets"], busy_score: null },

  { id: 7, name: "Asian", lat: 49.268453, lng: -123.245813, features: ["quiet", "outlets"], busy_score: null },

  { id: 8, name: "Xwi7xwa", lat: 49.264150, lng: -123.245500, features: ["quiet", "cultural"], busy_score: null },

  { id: 9, name: "Chapman", lat: 49.267950, lng: -123.251900, features: ["outlets", "group study"], busy_score: null },
];
