from fastapi.testclient import TestClient
from cmigrate.main import app

client = TestClient(app)


def test_runs_and_refuses_a_write():
    payload = client.post("/agent/run", json={"goal": 'plan the migration', **{'payload': {'services': [{'name': 'api'}, {'name': 'worker'}]}}}).json()
    assert payload["refused"] is False
    assert payload["applied"] is False
    assert payload["plan"] == ["api", "worker"]
    refused = client.post("/agent/run", json={"goal": 'switch dns cutover now'}).json()
    assert refused["refused"] is True
