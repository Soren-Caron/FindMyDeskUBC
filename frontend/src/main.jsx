/*
Spec (main entry file):

- Imports React StrictMode for highlighting potential issues.
- Imports Leaflet's CSS for map rendering and local global styles.
- Imports the main App component.
- Creates the React root using the #root DOM element.
- Renders <App /> inside <StrictMode> as the application root.
*/
import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import "leaflet/dist/leaflet.css";
import './index.css'
import App from './App.jsx'

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <App />
  </StrictMode>,
)
