FROM python:3.13.5-slim

RUN pip install --no-cache-dir websockets==17.0.1
ENV PYTHONHASHSEED=0

WORKDIR /app
COPY player.py /app/player.py
COPY library /app/library

CMD ["python", "/app/player.py"]
