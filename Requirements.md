
1. Map Display
  
   - The system should display an interactive map of the UBC Vancouver campus.
  
   - The map should visually represent study spaces as colored markers (green = high availability, red = low).
  
   - The map should automatically refresh displayed availability data at least every 60 seconds to 5 minutes (we have to decide this based on server load and performance).

   - The user shall be able to zoom in and out of the map. (still considering this option)

   - The user shall be able to click or tap a study spot marker to view details (features, ratings, current availability).
     

2. Search and Filtering
   
  2.1 Search
  
   - The system should lets users to query for study spaces by name or building.
  
   - The search should return relevant results ranked by proximity (still considering if we would want to add this feature) and availability.

  2.2 Filters

   - The user should be able to filter study spaces by features:
      - Quiet
      - Power outlets
      - Whiteboard
      - Group study space
      - Natural light
      - Spread of temporal availability
      - (We might decide to add more)

   - Filters should update the map and list view in real time.
  
   - Filters should be displayed and coded until the user clears them manually.

3. Availability and Prediction

   - Each study spot should display an Availability Status (Available, Busy, or Unknown).
  
   - Each study spot should include an Availability Score (0–100), computed from recent user check-ins and time-of-day trends and other data.
  
   - The system should estimate short-term availability predictions (next 2 hours) using statistical modeling.
  
   - Predicted availability shall be updated at least every 30 minutes.

4. User Interaction and Feedback

   - There should be a “check in” option for students.
  
   - When checking in, users may optionally submit feedback (e.g., noise level, plug availability, temperature, or crowding).
  
   - The feedback data must be stored anonymously.

   - The system will aggregate feedback data to improve availability predictions.

   - The feedback submission must be pretty concise.

5. Spot List & Ranking

   - The right-side panel will display a ranked list of study spots from most to least preferable.
  
   - The list will automatically refresh when filters are changed or feedback is received.

6. Data & Privacy

   - The system should not store any personally identifiable information (PII).
  
   - All feedback and check-in data will be anonymized before storage.
  
   - The system will use HTTPS for all communication between client and server.
  
   - User data will not be shared with third parties.

7.  AI / Prediction Logic

   - The AI model shall take in a bunch of factors that would dictate reliable study spots.

   - The model should output a normalized score between 0–100 for each spot.
  
   - Given new input, the model will recalibrate its model every 24 hours

