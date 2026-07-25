# main.py — the entry point of our FastAPI backend.
# This is the file Docker/Uvicorn will point at to actually run the API.

from fastapi import FastAPI

# FastAPI() creates the "application" object.
# Everything the API can do (routes, docs, middleware) attaches to this object.
app = FastAPI(title="Corax Arcana API")


# @app.get("/health") registers this function to run whenever someone
# sends an HTTP GET request to http://<our-server>/health
@app.get("/health")
def health_check() -> dict[str, str]:
    # "-> dict[str, str]" is a type hint: it tells Python (and FastAPI)
    # that this function returns a dictionary where both keys and values
    # are strings. FastAPI reads this hint to auto-generate API docs
    # and to validate the response shape.
    #
    # Why this matters for Data Engineering: pipelines and monitoring
    # tools will call endpoints like this to check "is the service up?"
    # before trying to pull or push data. A /health endpoint is the
    # standard, minimal contract every service in a data platform
    # is expected to expose.
    return {"status": "ok"}
