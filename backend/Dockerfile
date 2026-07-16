FROM python:3.12-slim
#Base image - a slim Debian with Python 3.12 pre-installed. Matches requires-python = ">=3.12" in pyproject.toml.

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/
#Grabs the uv binary directly from its own official image, instead of installing it via pip. Faster and is the pattern uv's own docs recommend.

WORKDIR /app
#Everything from here runs inside /app in the container — like cd /app.

COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-install-project
#Copy only the dependency files first, then install dependencies. This is deliberate ordering: Docker caches each layer, so if you only change your app code later (not dependencies), rebuilds skip straight past this slow step instead of reinstalling everything.

COPY . .
RUN uv sync --frozen
#Now copy the actual code, and finish syncing (installs your own project as editable).

CMD ["uv", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
#The command that runs when the container starts. --host 0.0.0.0 is required — without it, uvicorn only listens inside the container and Docker can't forward the port out to your machine.