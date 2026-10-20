import os
import uvicorn
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from workload_engine import WorkloadAnalyticsEngine
from data_generator import generate_workload_dataset

app = FastAPI(title="Employee Productivity vs Workload Intelligence")

if not os.path.exists("productivity_workload_data.json"):
    generate_workload_dataset(150)

engine = WorkloadAnalyticsEngine()

@app.get("/", response_class=HTMLResponse)
async def serve_index():
    with open("templates/index.html", "r", encoding="utf-8") as f:
        return f.read()

@app.get("/api/workload")
async def get_workload():
    return engine.analyze_bottlenecks()

@app.post("/api/recalculate")
async def recalculate():
    generate_workload_dataset(150)
    global engine
    engine = WorkloadAnalyticsEngine()
    return {"status": "success", "message": "Re-simulated workload records."}

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8005, reload=True)
