# syntax=docker/dockerfile:1
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app/04_Execution_Engine:/app/04_Execution_Engine/LangGraph_Pipelines

WORKDIR /app

COPY 04_Execution_Engine/requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir --requirement /tmp/requirements.txt

COPY 02_Organization_and_Roles /app/02_Organization_and_Roles
COPY 03_Knowledge_Base_RAG /app/03_Knowledge_Base_RAG
COPY 04_Execution_Engine /app/04_Execution_Engine

RUN useradd --create-home --uid 10001 triton
USER triton

CMD ["python", "04_Execution_Engine/LangGraph_Pipelines/master_graph.py", "--demo"]
