# TESTING.md — Backend Testing Documentation

## Overview

This document describes the testing setup for the FindMyDesk UBC Backend, including:

- what is being tested  
- how the test suite is organized  
- how the tests are executed  
- how external dependencies (weather API, file system, training pipeline) are mocked  
- how the environment is configured so pytest can import backend modules correctly  

The goal of the test suite is to verify correctness, stability, and reproducibility of the backend logic that predicts desk busyness across UBC libraries.

---

# Folder Structure

backend/
│
├── main.py
├── model.py
├── weather.py
├── lookup.json
├── tests/
│   ├── test_API.py
│   ├── test_Training.py
│   ├── test_Utils.py
│   └── test_training_pipeline.py
│
└── __init__.py

All automated tests live inside backend/tests/.

---

# Testing Framework

We use:

### pytest
A lightweight and powerful Python testing framework.

Run all tests:

    pytest -v

Run tests inside backend only:

    cd backend
    pytest -v

---

# Import Fix — Making backend testable

Python normally cannot import modules like:

    from backend.model import ...

when tests run from inside the backend/ folder.

To solve this, we added:

    __init__.py

and inserted the backend path manually inside each test file:

import sys
from pathlib import Path

BACKEND_DIR = Path(file).resolve().parents[1]
if str(BACKEND_DIR) not in sys.path:
sys.path.insert(0, str(BACKEND_DIR))


This guarantees pytest can always import `main` and `model`, no matter where tests are run from.

---

# Test Categories

## 1. Utility Function Tests (test_Utils.py)

These tests verify small, deterministic helper functions:

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

## 2. Model Training Tests (test_Training.py)

These tests check the model training phase:

- verifies that train_model() reads desk logs correctly  
- ensures lookup.json is generated  
- ensures its structure includes:
  - per_library  
  - global  

We use tmp_path to create temporary CSV files so tests never modify the real dataset.

---

## 3. Prediction Pipeline Tests (test_training_pipeline.py)

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

## 4. API Tests (test_API.py)

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

# Mocking Strategy

Mocking is essential because we do not call external systems during tests.

We mock:

Weather API:

monkeypatch.setattr("model.get_weather", fake_weather)

Feedback lookup:


This makes all tests fast, isolated, and reproducible.

---

# Test Results

After fixing imports and path issues, all tests now pass:

    15 passed in 0.81s

This confirms the backend is fully test-covered and functioning.

---

# Future Improvements

If time permits, consider:

- Adding coverage analysis (pytest --cov)
- Adding CI/CD automation (GitHub Actions)
- Stress-testing with large datasets
- Adding type checks with mypy

---

# Summary

The backend now has:

- Complete test suite  
- Proper mocking of dependencies  
- Correct import structure  
- Full model + API test coverage  

This makes the system stable, maintainable, and ready for demo or deployment.

