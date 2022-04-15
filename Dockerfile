# Please note this Dockerfile requires BuildKit available with Docker
ARG BUILD_IMAGE='prod'

FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9 as base_image

WORKDIR /app/

# Install Poetry
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | POETRY_HOME=/opt/poetry python && \
    cd /usr/local/bin && \
    ln -s /opt/poetry/bin/poetry && \
    poetry config virtualenvs.create false

# Copy poetry.lock* in case it doesn't exist in the repo
COPY ./pyproject.toml ./poetry.lock* /app/

FROM base_image AS dev-version
# Install production and development dependencies
RUN poetry install --no-root

FROM base_image AS prod-version
# Install only production dependencies
RUN poetry install --no-root  --no-dev
COPY version.json /app/app/version.json
COPY Makefile /app/Makefile

# Add aptible-required deployment items
RUN mkdir /.aptible/
COPY Procfile /.aptible/

FROM ${BUILD_IMAGE}-version AS final_image
RUN apt-get remove -y gcc

COPY ./app /app
COPY ./start.sh /start.sh
RUN chmod +x /start.sh

ENV PYTHONPATH=/app
