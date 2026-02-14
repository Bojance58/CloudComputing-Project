FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY main.py .

# Azure Web App container port
ENV PORT=8080
EXPOSE 8080

CMD ["sh", "-c", "gunicorn -w 2 -k gthread --threads 8 -b 0.0.0.0:${PORT} main:app"]
