FROM python:3.12-slim-buster as base

ENV PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONHASHSEED=random \
  PIP_NO_CACHE_DIR=off \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_DEFAULT_TIMEOUT=100 \
  POETRY_NO_INTERACTION=1 \
  POETRY_VIRTUALENVS_CREATE=false \
  POETRY_CACHE_DIR='/var/cache/pypoetry' \
  POETRY_HOME='/usr/local' \
  POETRY_VERSION=1.8.1

# Install poetry
RUN apt-get update -qq && apt-get install -y --no-install-recommends curl
RUN curl -sSL https://install.python-poetry.org | python3 -

# Set workdir and copy project
WORKDIR /app
COPY . .

# Creation of virtual env is automatically handled by poetry
# Install dependencies managed by Poetry
RUN poetry config virtualenvs.create false
RUN poetry install --no-interaction --no-ansi --no-root

# Use a new light image to transfer build
FROM base as final

# Setting working directory
WORKDIR /app

# Transfering built poetry env from previous stage
COPY --from=base /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages/

# Copying project files
COPY . .
# RUN chmod +x ./scripts/start_flower.sh

# RUN chmod g-rw acme.json
# Setting the entry point of the app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

# Exposing default port for FastAPI
EXPOSE 8000