"""
Spec:
- GET , health check, returns {"status": "backend running"}
- GET /train, runs train_model(), returns message + entry counts
- GET /predict?spot=...&timestamp=..., predicts busy score using predict_busy_score()
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from model import train_model, predict_busy_score

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],         
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
  return {"status": "backend running"}


@app.get("/train")
def train():

  result = train_model()
  return {
    "message": "training complete",
    "per_library_entries": sum(len(v) for v in result["per_library"].values()),
    "global_entries": len(result["global"])
  }


@app.get("/predict")
def predict(spot: str, timestamp: str | None = None):
  return predict_busy_score(spot, timestamp)
