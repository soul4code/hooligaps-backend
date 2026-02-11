FROM python:3.13-slim

RUN apt-get update && apt-get install -y \
    build-essential \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*


RUN pip install --no-cache-dir poetry

WORKDIR /app

COPY . .

ENV POETRY_VIRTUALENVS_CREATE=false
ENV POETRY_HOME=/opt/poetry
ENV PATH="$POETRY_HOME/bin:$PATH"

RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1


EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
