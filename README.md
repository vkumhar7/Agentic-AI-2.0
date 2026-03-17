# Agentic Financial Risk Analysis Framework

This project provides an **agentic framework** for automated portfolio risk analysis and narrative commentary generation.

## Stack
- **API layer:** FastAPI
- **Data validation / contracts:** Pydantic v2
- **Containerization:** Docker
- **Deployment target:** Kubernetes

## Agentic workflow
The service uses a simple orchestrator (`RiskAnalysisOrchestrator`) that coordinates three domain-specific agents:

1. **MarketRiskAgent**
   - Calculates per-position VaR(95), expected credit loss, and liquidity penalty.
2. **PortfolioAggregatorAgent**
   - Aggregates position-level outputs into portfolio-level risk metrics and assigns a risk band.
3. **CommentaryAgent**
   - Produces structured human-readable commentary for decision support.

## API Endpoints
- `GET /health` — health probe endpoint.
- `POST /analyze` — evaluate portfolio risk and generate commentary.

### Example request
```json
{
  "portfolio_name": "Global Macro Book",
  "positions": [
    {
      "symbol": "AAPL",
      "exposure_type": "market",
      "notional_usd": 2000000,
      "volatility": 0.22,
      "probability_of_default": 0.01,
      "loss_given_default": 0.30,
      "liquidity_horizon_days": 3
    }
  ]
}
```

## Local development
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Run tests:
```bash
pytest -q
```

## Docker
Build and run locally:
```bash
docker build -t risk-analysis-api:local .
docker run --rm -p 8000:8000 risk-analysis-api:local
```

## Kubernetes deployment
Update image reference in `k8s/deployment.yaml`, then apply:
```bash
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
kubectl apply -f k8s/ingress.yaml
```

## Repository structure
```
app/
  agents.py
  engine.py
  main.py
  models.py
k8s/
  deployment.yaml
  service.yaml
  ingress.yaml
tests/
  test_api.py
Dockerfile
requirements.txt
```
