from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health() -> None:
    response = client.get('/api/health')
    assert response.status_code == 200
    assert response.json()['status'] == 'ok'


def test_dashboard_page() -> None:
    response = client.get('/')
    assert response.status_code == 200
    assert 'CrowdPilot AI' in response.text


def test_gates_api() -> None:
    response = client.get('/api/gates')
    assert response.status_code == 200
    assert len(response.json()) >= 1


def test_create_alert() -> None:
    payload = {'title': 'Test alert', 'message': 'Route users to Gate 4.', 'severity': 'medium'}
    response = client.post('/api/alerts', json=payload)
    assert response.status_code == 200
    assert response.json()['title'] == payload['title']


def test_ai_summary() -> None:
    response = client.get('/api/ai/summary')
    assert response.status_code == 200
    assert 'summary' in response.json()
