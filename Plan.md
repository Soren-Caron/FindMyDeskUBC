Who coordinates the work
1.1 Roles and responsiblities simplified

  - The project manager (PM) - Soren:
    - Plans the meetings and process. Does risk management and stakeholder communication. Will also help in programming.

  - Designer - Samuel:
    - Plans the visual style and accessibility rules. Leads the UX/UI and tests the programs usibility via the front end.

  - Programmer - Jason, Dow, Daniel 
    - Implement frontend (MapView, ListView, FeedbackForm), backend API (AI implementation).

1.2 PM Practices and workflow

  - Everything will be posted here on github, such as our code or planning (REQUIREMENTS.md, ARCHITECTURE.md, and PLAN.md).
  - There is a seperate google docs called the issues form keeps track of what needs to be done and who is doing it.
  - In the same google docs at the top we have a table to show progress and productivity with the following:
    - To Do: what we’ll do next
    - In Progress: what someone’s working on right now
    - In Review: finished work waiting for someone to check
    - Done: finished and working
  - We have our own repo where we code on. In that repo we have a main branch that nobody touches. We create our own seperate branches and finally implement it when ready. This repo is only for handing assignments in.
  - How we know when a task is truly done:
    - The code works
    - Someone has reviewed or tested it
    - Passes all the test benches
    - When merged, nothing breaks

1.3 Meetings

  - Regular Meetings every 3-4 days that last about 30 minutes to check how everyone is doing. PM leads the discussion here.
  - Twice a week we have 2-3 hour meeting where we discuss the code. The developers lead the discussion here while PM plans
  - Design review: we will plan a weekly design review about 2-3 hours to discuss the current design, check if we should implement anything new, bugs, etc. Designer leads the discussion here while PM plans.
  - Near the end fo the product implementation or prototype, there will be a meeting to test the product.





2. Communication tools & reasons

  - GitHub — Showcase code and branches
    - Why: Required for submission and traceable history of code

  - Instagram / Discord — Real-time chat (#general, #dev, #design, #urgent).
    - Why: Fast and efficient means of communication. Urgent messages are also recieved quickly

  - Zoom / Google Meet — Video meetings and screen sharing.
    - Why: Live design walkthroughs and demos.

  - Figma — UI mockups
    - Why: Designer needs a collaborative canvas to work on and showcase designs;

  - Google Drive — Long form docs, meeting notes, or large files.
    - Why: Easy sharing and backup.








3. Component Ownership (one main person per part)
  "Owning them means being responsible for writing them and making sure they are functional and correct."

  Frontend Components 

    - MapView — Jason (Developer)
      - Jason will use javascript leaflet (we might change this) to program the map interface. Also add colour-coded zones (green = good, red = bad), and handle map clicks.
    
    - SpotListView — Daniel (Developer)
      - Daniel will code the list that is displayed on the right hand side, showing all study spots ranked from best to worst.
      - By clicking one of the items, user will be zoomed the map to that spot.
    
    SpotDetailView & Prediction Bar (display certainty maybe) — Soren (PM)
      - Shows details about each study space and a short-term prediction (next 2 hours).
    
    FeedbackFormView — Samuel (Designer) + Dow (Developer)
      - Samuel designs how the interface looks and logic of it.
      - Dow codes the form that lets users check in, leave feedback, and update the availability.
    
    FilterBarView — Samuel (Designer) and Daniel (Developer)
      - Adds checkboxes for simple filters like “Quiet,” “Has Outlets,” or “Natural Light.”
      - Samuel plans the look and feel; Daniel connects it to the backend filters.


  Backend Components

    - ClientModel (Local Data + Updates) — Dow (Developer)
      - Responsible for taking care of local data in the browser and to make the user interface as quick as possible when a request is sent.

    - APIClient (Frontend-Backend Connection) — Jason (Developer)
      - Basically controls all requests between the website and the server:
      - In case something goes wrong, there is a basic retry logic.

    - SpotController (Server) — Daniel (Developer)
      - The component that is responsible for retrieving and returning all the studyspots.

    - FeedbackController (Server) — Dow (Developer)
      - Handles saving user check-ins and feedback. Validates and stores the data safely.

    - AggregateService (Availability & Predictions) — Soren (PM) + Jason (Developer)
      - Uses both feedback data with time-of-day trends to calculate a “preference score.”
      - Gives short-term predictions depending on all the data it has.
      - To train this AI model, we will use historical data and user feedback (anonymous of course).



4. Timeline:
  - Nov 10th - Find data to train the AI model
    - Find data from API such as Google Maps, weather apps, etc.
    - Find historical data to train current model.
    - Do independent research by going to libraries or asking peers.
  - Nov 12th - Build Basic Functions
    - Code basic methods to retrieve the data for the map and list.
    - Show the map with a few test spots and the list beside it (just a few spots for now with random satisfaction score).
    - Check if clicking on a spot actually works (shows details).
    - Create test cases to make sure these work.
  - Nov 15th - Add Feedback & Test Cases
    - Code the feedback form so users can report what spot they went to and when.
    - Write test cases to check that feedback is saved correctly.
    - Update the map/list using feedback (colors or scores change). (Logic will change once we implement AI.)
  - Nov 18th - Code the AI logic
    - Create the AI that is capable of predicting the satisfaction score accurately.
    - Create a bunch of test cases to make sure this works.
  - Nov 21st - Final Logic & Polish
    - Create the scoring logic so spots are ranked automatically.
    - Add finishing small UI improvements (colors, layout, mobile view).
    - Do final black-box testing to make sure the web works as intended.





5. How we will verify project works - For the following are just otherways we can test the product aside from test cases:

  - Map Display
     
    - Interactive map of UBC campus
      - Test: Load the map on both desktop and mobile. See if the map of the campus is shown.
      - Pass: Map appears and is readable.
      - Tester: Jason, Daniel
        
    - Coloured spots for study locations (green = high availability, red = low)
      - Test: Add study spaces with loaded satisfaction score and check the colour.
      - Pass: Colours match the expected expected colours.
      - Tester: Jason
  
    - Automatic refresh of availability data (every 1–5 min)
      - Test: Wait and confirm the map updates without reloading the page.
      - Pass: Map refreshes on time and displays correct scores. We may need to brute force new data for this test
      - Tester: Dow
  
    - Zoom in/out (we are still considering if we want to implement this)
      - Test: Attempt to zoom using buttons or gestures.
      - Pass: Map zooms in and out smoothly.
      - Tester: Daniel
  
    - Click/tap marker to view details
      - Test: Click on a location to check that location's features, ratings, and availability appear.
      - Pass: All locations show correct info.
      - Tester: Soren
  
  - Search and Filtering
     
    - Search
      - Query by study space name or building
        - Test: Type known names and buildings into the search box. 
        - Pass: Results match query.
        - Tester: Samuel

    - Filters
      - Filter by features (quiet, plugs, whiteboard, etc.)
        - Test: Do each possible combination of filters or random combinations if the number of filters get too large.
        - Pass: Only spots with selected features appear on map and list.
        - Tester: Daniel
  
      - Filters update in real time
        - Test: Change filters and confirm map/list updates immediately (or atleast quickly).
        - Pass: Updates occur without page reload.
        - Tester: Daniel
  
      - Filters remain until cleared
        - Test: Apply filters, Do random activites around the website, return to view.
        - Pass: Check if the filters are always there
        - Tester: Daniel
  
  - Availability and Prediction
     
    - Short-term availability prediction (next 2 hours)
      - Test: Input historical data, run prediction function, compare with expected trend.
      - Pass: Predicted availability is reasonable and updates every 30 minutes (might change).
      - Tester: Soren

  - User Interaction and Feedback (rest is covered in other parts)
     
    - Check-in option
      - Test: Submit feedback and check-ins for test spots.
      - Pass: Anonymous data are recorded in the database.
      - Tester: Soren

  - Spot List & Ranking
     
    Right-side panel shows ranked list
      - Test: Have a bunch of items in the list. Compare list order with computed availability scores.      
      - Pass: List matches expected ranking. 
      - Tester: Daniel

    List updates with filters or new feedback 
      - Test: Apply filters and submit feedback, confirm list updates.
      - Pass: List updates immediately to match current data.      
      - Tester: Daniel

  - Data & Privacy
     
    - No personal information is stored
      - Test: Inspect database/logs.     
      - Pass: nothing suspicious found.
      - Tester: Soren
    
    - Anonymized feedback/check-ins
      - Test: Submit a feedback and check the storage.
      - Pass: Feedback has no user info.     
      - Tester: Dow   

    - HTTPS communication
      - Test: Open app in browser, check URL and network requests.  
      - Pass: HTTPS active for all connections.      
      - Tester: Soren  

  - AI / Prediction Logic
     
    - Score output 0–100 for each spot  
      - Test: Provide a known input and check output score range.  
      - Pass: Score is between 0–100.
      - Tester: Soren
      
    - Recalibrate model every 24 hours
      - Test: Simulate that 24-hour is happened to showcase the update and check model output.
      - Pass: Model updates successfully without errors.
      - Tester: Soren

    - Availability Score and other scores (potentially)
      - Test: Provide a set of inputs, check if the output is reasonable.
      - Pass: Scores match expected values.
      - Tester: Soren




** IMPORTANT: ANYTHING ABOVE IS NOT FINALIZED AND IS SUBJECT TO CHANGE IN THE FUTURE
