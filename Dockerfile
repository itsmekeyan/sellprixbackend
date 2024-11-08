FROM python:3.11.4-slim-bullseye AS prod

RUN pip install poetry==1.8.2

# Configuring poetry
RUN poetry config virtualenvs.create false
RUN poetry config cache-dir /tmp/poetry_cache

# Copying the entire project
COPY . /app/src/
WORKDIR /app/src

# Regenerate the lock file and install dependencies
RUN --mount=type=cache,target=/tmp/poetry_cache \
    poetry lock --no-update && \
    poetry install --only main --no-root

CMD ["/usr/local/bin/python", "-m", "fast_api"]

FROM prod AS dev

RUN --mount=type=cache,target=/tmp/poetry_cache poetry install