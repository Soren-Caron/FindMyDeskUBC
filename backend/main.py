from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from model import train_model, predict_busy_score

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],          # allow all sources (localhost:5173)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
  return {"status": "backend running"}


@app.get("/train")
def train():
  """
  Train the simple 3-hour-bin model from desk_logs.csv.
  Also computes global pattern for fallback.
  """
  result = train_model()
  return {
    "message": "training complete",
    "per_library_entries": sum(len(v) for v in result["per_library"].values()),
    "global_entries": len(result["global"])
  }


@app.get("/predict")
def predict(spot: str, timestamp: str | None = None):
  """
  Predict busyness for a study spot at a given time.
  - spot: e.g. "IKBLC", "Koerner", "Woodward"
  - timestamp: ISO string, e.g. 2025-02-14T14:00 (optional, defaults to now)
  """
  return predict_busy_score(spot, timestamp)
