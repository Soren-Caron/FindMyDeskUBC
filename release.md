How to install and use

  1. Our product is currently at a very healthy stage. We would like to further polish it and make it better before actually publishing it on the internet. So the current temporary way of interacting with it is as follows:
  2. Clone the repo in your personal hardware system and open it in an IDE such as visual studio.
  3. Make sure to have python 3.11 installed. Then make sure to install node.js with the npm package manager. 
  4. Then from there, got to “cd FindMyDeskUBC/backend” and create a venv with “python3 -m venv venv”. Finally, activate it “source venv/bin/activate” in non- windows and “.\venv\Scripts\Activate.ps1” in windows. make sure you are able to see “(venv)”
  5. Now install the backend dependencies:
     pip install fastapi uvicorn pandas python-dateutil requests  
     pip install python-dotenv  
     pip install uvicorn fastapi pandas requests python-dotenv
  6. Open two separate terminal tabs. In one go to backend folder and then run “python -m uvicorn main:app --reload”
  7. In the other terminal tab go to the frontend and then run “npm install” and then run command “npm run dev”.

How we tested the product:

  The testing was carried carried out differently across frontend and backend. We used pathlib to test python code. We also used coverage.py to check code coverage and we scored about 73% branch coverage. Read README_TESTING_DOCUMENTATION.md for more information.
  Front end creating designed tests was difficult. As a result we decided to check the website itself. We played around with it each time we changed it, checking many different ways and edge cases to look for ways the code could break or result in unpredictable behaviours. 

Known Bugs and future expectations:

  First time opening the website the business score is not shown. The website needs to be refreshed first.
  The locations of the libraries are not accurate.
  More locations can be added like the nest or faculty. 
  The lists of libraries on the left should be ordered top to bottom.
  Filters could be more accurate. We’ll do some research to see how the filters fit.
  Map is slow or laggy sometimes. Probably caused by large JSON files/too many markers. Will fix in the future by using MarkerClusterer and canvas rendering when possible. 

Contribution statement

  Soren (Project Manager)
  
   Oversaw overall system architecture, coordinating the integration of the FastAPI backend, prediction model, and React/Vite frontend.
    Built major backend components including the ML-based busy-score model, lookup.json training pipeline, and /predict API endpoint.
    Implemented backend features such as weather-aware predictions, timestamp parsing, data cleaning, and feedback integration logic.
    Helped connect the frontend to the backend by designing the API format and ensuring consistent data structures across the system.
    Guided team direction, debugging sessions, and final deployment-readiness review.

Jason (Developer)

  Developed the interactive campus map using React + Leaflet, including markers, auto-zooming, and dynamic coloring tied to live busy scores.
  Implemented the busy score fetching logic in the UI, ensuring all study spots automatically pull predictions from the FastAPI backend on page load.
  Built reusable frontend utilities for API requests and error handling.
  Collaborated on state management for globally storing live spot data and ensuring smooth updates across the interface.

Daniel (Developer)

  Implemented the Sidebar Spot List, including search, filtering, sorting, and integration with map interactions.
  Connected Samuel’s filter designs to functional code, enabling real-time filtering by features (Quiet, Outlets, Group Study, etc.).
  Assisted with frontend–backend integration through the shared spotsData state system, ensuring UI components always reflect live prediction values.

Samuel (Designer)

  Led the design of all major interface components, including the Sidebar, Feedback Panel, and overall visual layout.
  Created user-centered flows for feedback submission, spot browsing, and selecting study spaces.
  Provided consistent styling direction and UI refinement across the map view, spot list, and forms.
  Ensured the frontend maintained a cohesive, intuitive experience across desktop and mobile layouts.

Dow (Developer)

  Implemented the Feedback Panel functionality, including sending feedback to Supabase and retrieving historical ratings.
  Developed the Client Session Model, enabling anonymous, persistent user sessions via localStorage.
  Built the backend portion of the feedback pipeline, validating and formatting feedback for ML integration.
  Ensured the busy-score model correctly includes user sentiment as a real-time adjustment to predictions.
