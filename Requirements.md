
1. Core Map Interface
  1.1 Map Display
  
  REQ-1.1.1: The system shall display an interactive map of the UBC Vancouver campus.
  
  REQ-1.1.2: The map shall visually represent study spaces as colored markers (green = high availability, red = low).
  
  REQ-1.1.3: The map shall automatically refresh displayed availability data at least every 60 seconds.
  
  REQ-1.1.4: The user shall be able to zoom in and out of the map.
  
  REQ-1.1.5: The user shall be able to click or tap a study spot marker to view details (features, rating, current availability).

2. Search and Filtering
  2.1 Search
  
  REQ-2.1.1: The system shall allow users to search for study spaces by name or building.
  
  REQ-2.1.2: The search shall return relevant results ranked by proximity and availability.

  2.2 Filters
  
  REQ-2.2.1: The user shall be able to filter study spaces by features:

    Quiet
    
    Power outlets
    
    Whiteboard
    
    Group study space
    
    Natural light
    
    24/7 access

  REQ-2.2.2: Filters shall update the map and list view in real time.
  
  REQ-2.2.3: Filters shall persist until the user clears them manually.

3. Availability and Prediction

  REQ-3.1.1: Each study spot shall display an Availability Status (Available, Busy, or Unknown).
  
  REQ-3.1.2: Each study spot shall include an Availability Score (0–100), computed from recent user check-ins and time-of-day trends.
  
  REQ-3.1.3: The system shall estimate short-term availability predictions (next 2 hours) using lightweight statistical modeling.
  
  REQ-3.1.4: Predicted availability shall be updated at least every 30 minutes.

4. User Interaction and Feedback

  REQ-4.1.1: The user shall be able to “check in” to a study spot.
  
  REQ-4.1.2: When checking in, users may optionally submit feedback (e.g., noise level, plug availability, temperature, or crowding).
  
  REQ-4.1.3: Feedback data shall be stored anonymously.
  
  REQ-4.1.4: The system shall aggregate feedback data to improve availability predictions.
  
  REQ-4.1.5: The feedback submission form shall require less than 3 clicks or taps to complete.

5. Spot List & Ranking

  REQ-5.1.1: The right-side panel shall display a ranked list of study spots from most to least preferable.
  
  REQ-5.1.2: Ranking shall be based on current availability, user feedback, and average ratings.
  
  REQ-5.1.3: The list shall automatically refresh when filters are changed or feedback is received.

6. Data & Privacy

  REQ-6.1.1: The system shall not store any personally identifiable information (PII).
  
  REQ-6.1.2: All feedback and check-in data shall be anonymized before storage.
  
  REQ-6.1.3: The system shall use HTTPS for all communication between client and server.
  
  REQ-6.1.4: User data shall not be shared with third parties.

7. System Performance

  REQ-7.1.1: The main map and list page shall load within 3 seconds on a standard UBC Wi-Fi connection.
  
  REQ-7.1.2: The app shall be responsive on both desktop and mobile browsers.
  
  REQ-7.1.3: The system shall recover gracefully from network interruptions.

8.  AI / Prediction Logic

  REQ-8.1.1: The AI module shall compute a weighted average of:
  
    Recent user check-ins (past 60 minutes)
    
    Historical averages by time and weekday

  REQ-8.1.2: The model shall output a normalized score between 0–100 for each spot.
  
  REQ-8.1.3: The system shall allow retraining or recalibration every 24 hours.

9. Testing & Verification

  Each requirement above shall be verified through one or more of the following methods:
  
  Unit testing (front-end and back-end)
  
  Integration testing (map + data + feedback flow)
  
  User testing (UX validation)
  
  Manual inspection (performance and security checks)
