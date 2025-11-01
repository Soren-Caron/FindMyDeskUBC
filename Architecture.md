Model:
1. StudySpotModel
  -   Responsibility: Stores all information about UBC study spots (location, capacity, features, historical availability data, etc.).
  -   Location: Server
  -   Communicates with: Spotcontroller to obtain and update spot data, and a database
2. UserFeedbackModel
  -   Responsibility: Stores the feedback submitted by users about study spaces with time that it was sent and the location.
  -   Location: Server
  -   Communcates with: FeedbackController and a database
3. UserSessionModel
  -   Tracks user (anonymous of course) check-ins, bookmarked spots, and preferences during a session.
  -   Location: Client
  -   Communicates with: UIController and SpotController
4. PredictionModel
  -   An AI prediction model computes availability for each possible study spot. Use crowdsourced and historical data.
  -   Location: Server
  -   Communicates with: StudySpotModel and SpotController

Controller:
1. SpotController
  - Responsibility: Provides the application logic for retrieving, sorting, and filtering study spots.
  - Location: Server
  - Communicates with: StudySpotModel, PredictionModel, UserSessionModel, MapView, ListView

3. FeedbackController
  - Responsibility: Controls submission and retrieval of feedback from users.
  - Location: Server
  - Communicates with: UserFeedbackModel and FeedbackFormView
5. UIController
  - Responsibilty: Controls client-side interactions between user actions, map, and stored data. Allows event listeners for clicks, filters, and feedback submissions.
  - Location: Client
  - Communicates with: MapView, ListView, FeedbackFormView, SpotController, UserSessionModel

Views:
1. MapView
  - Responsibility: Displays the UBC campus map with colored indicators showing study spots (green = available, red = busy). Allows users to click a spot to view details.
  - Location: Client
  - Communicates with: UIController, SpotController
2. ListView
  - Responsibility: Shows a ranked list of study spots (most to least preferable).
  - Location: Client
  - Communcates with: UIController, SpotController
3. FeedbackFormView
  - Responsibility: Collects user feedback (spot name, time, comments) and sends it to the backend.
  - Location: Client
  - Communicates with: UIController, FeedbackController
4. FilterBarView
  - Responsibility: Allows users to filter spots.
  - Location: Client
  - Communicates with: UIController, ListView, MapView
