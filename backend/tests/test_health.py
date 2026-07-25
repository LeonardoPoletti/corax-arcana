# test_health.py — verifies the /health endpoint works as expected.
# pytest auto-discovers this file because its name starts with "test_".

from fastapi.testclient import TestClient

# TestClient lets us call our FastAPI routes in memory, without starting
# a real server or opening a network port. It's built on top of httpx,
# which is why we installed httpx as a dev dependency.
from app.main import app

# Import the actual FastAPI app instance built in main.py — the one
# that already has the /health route registered on it.

client = TestClient(app)
# Wrap the app in a fake client. Calling client.get(...) behaves like a
# real HTTP GET request, but runs entirely inside this process — fast,
# no network involved.


def test_health_check():
    # pytest treats any function starting with "test_" as a test case,
    # discovered automatically — no manual registration needed.

    response = client.get("/health")
    # Simulate a GET request to /health, exactly like a browser or a
    # monitoring tool would send against a real running server.

    assert response.status_code == 200
    # 200 means "OK" — the request succeeded. If health_check() ever
    # raised an exception internally, this would catch it by failing
    # with a different status code (likely 500).

    assert response.json() == {"status": "ok"}
    # Confirm the response body matches exactly what health_check()
    # returns in main.py. If someone changes that return value without
    # updating this test, this assertion is what catches the mismatch.
