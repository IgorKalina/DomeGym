ARG PYTHON_VERSION=3.11.10
FROM python:${PYTHON_VERSION}-slim AS app_build

ARG POETRY_VERSION=1.8.4

WORKDIR /tmp
RUN pip install --no-cache-dir "poetry==${POETRY_VERSION}"
COPY pyproject.toml ./poetry.lock* /tmp/

RUN poetry export -f requirements.txt --output requirements.txt --without-hashes \
  && pip install --no-cache-dir --upgrade -r requirements.txt


# Final distroless image
FROM gcr.io/distroless/python3-debian12:nonroot AS app_distroless_build
ARG PYTHON_VERSION=3.11
COPY --from=app_build /usr/local/lib/python${PYTHON_VERSION}/site-packages /usr/local/lib/python${PYTHON_VERSION}/site-packages

# Copy only files required for runnning the application
COPY src /app/src
COPY configs /app/configs

WORKDIR /app

ENV PYTHONPATH=/usr/local/lib/python${PYTHON_VERSION}/site-packages:/app
EXPOSE 8000
CMD ["src/gym_management/presentation/api/main.py"]
