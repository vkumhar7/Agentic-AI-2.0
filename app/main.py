from __future__ import annotations

from fastapi import FastAPI

from .engine import RiskAnalysisOrchestrator
from .models import AnalysisResponse, PortfolioInput

app = FastAPI(
    title="Agentic Financial Risk Analysis API",
    version="1.0.0",
    description="Automated portfolio risk analysis and commentary generation.",
)

orchestrator = RiskAnalysisOrchestrator()


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/analyze", response_model=AnalysisResponse)
def analyze_portfolio(payload: PortfolioInput) -> AnalysisResponse:
    return orchestrator.run(payload)
