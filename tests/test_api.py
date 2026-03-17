from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_health() -> None:
    response = client.get('/health')
    assert response.status_code == 200
    assert response.json() == {'status': 'ok'}


def test_analyze_portfolio() -> None:
    payload = {
        'portfolio_name': 'Global Macro Book',
        'positions': [
            {
                'symbol': 'AAPL',
                'exposure_type': 'market',
                'notional_usd': 2_000_000,
                'volatility': 0.22,
                'probability_of_default': 0.01,
                'loss_given_default': 0.3,
                'liquidity_horizon_days': 3,
            },
            {
                'symbol': 'HY_BOND_ETF',
                'exposure_type': 'credit',
                'notional_usd': 1_200_000,
                'volatility': 0.18,
                'probability_of_default': 0.05,
                'loss_given_default': 0.45,
                'liquidity_horizon_days': 9,
            },
        ],
    }

    response = client.post('/analyze', json=payload)
    assert response.status_code == 200

    data = response.json()
    assert data['portfolio_name'] == payload['portfolio_name']
    assert data['summary']['risk_band'] in {'low', 'moderate', 'high', 'critical'}
    assert len(data['position_breakdown']) == 2
    assert len(data['commentary']) == 3
