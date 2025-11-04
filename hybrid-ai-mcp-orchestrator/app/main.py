from fastapi import FastAPI
from pydantic import BaseModel
from app import analyzer, hardware_recommender

app = FastAPI(title="Hybrid AI MCP Orchestrator")

class AnalyzeRequest(BaseModel):
    code: str

class AnalyzeResponse(BaseModel):
    algorithms: list[str]

class HardwareRequest(BaseModel):
    algorithm: str

class HardwareResponse(BaseModel):
    suggested_hardware: str
    reasoning: str

@app.get("/")
def root():
    return {"message": "Hybrid AI MCP Orchestrator is running."}

@app.post("/analyze_program", response_model=AnalyzeResponse)
def analyze_program(req: AnalyzeRequest):
    algos = analyzer.detect_algorithms(req.code)
    return AnalyzeResponse(algorithms=algos)

@app.post("/recommend_hardware", response_model=HardwareResponse)
def recommend_hardware(req: HardwareRequest):
    suggestion = hardware_recommender.recommend_for_algorithm(req.algorithm)
    return suggestion
