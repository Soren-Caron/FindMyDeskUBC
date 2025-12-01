TESTING.md — Backend Testing Documentation

The testing folder consists of three tests using pytest as the testing framework.
to run all tests do:
pytest -v
to run tests in backend
cd backend
pytest -v

**Note we added an empty python folder "__init__.py"
as python can't import module by "from backend.model import"

so we inserted the backend path manually inside each test file:
import sys
from pathlib import Path
BACKEND_DIR = Path(file).resolve().parents[1]
if str(BACKEND_DIR) not in sys.path:
sys.path.insert(0, str(BACKEND_DIR))
This guarantees pytest can always import `main` and `model`, no matter where tests are run from.

---
**Note Chatgpyt was used to help generate some of the test cases.
*These tests were mainly written to catch bugs in our code

Test Categories

1. Utility Function Tests (test_Utils.py)

These tests verify small helper functions:

- normalize_desk_to_library()
- get_bin_from_hour()
- apply_weather_adjustment()
- get_feedback_score()

Mocking is used to simulate:

- weather API failure  
- weather with rain  
- feedback CSVs created at runtime  

These tests validate correctness of transformation logic and edge-case handling.

---

2. Model Training Tests (test_Training.py)

These tests check the model training phase:

- verifies that train_model() reads desk logs correctly  
- ensures lookup.json is generated  
- ensures its structure includes:
  - per_library  
  - global  

We use tmp_path to create temporary CSV files so tests never modify the real dataset.

---

3. Prediction Pipeline Tests (test_training_pipeline.py)

Validates the full prediction pipeline with mocked components:

- mocked lookup.json  
- mocked feedback  
- mocked weather  
- prediction returns:
  - model score  
  - feedback score  
  - adjusted score  

Ensures robustness even when external systems fail or return special values.

---

4. API Tests (test_API.py)

We use FastAPI’s TestClient to simulate real HTTP requests.

Endpoints tested:

### `/`
Checks backend is running.

### `/predict` success
Mocks model + weather + feedback → ensures API returns a valid prediction.

### `/predict` when lookup.json is missing
Intentionally forces the model to throw FileNotFoundError and verifies the API handles it correctly.

This guarantees predictable API behavior.

---

After fixing imports and path issues, all tests now pass:

    15 passed in 0.81s

This confirms the backend is fully test-covered and functioning.


