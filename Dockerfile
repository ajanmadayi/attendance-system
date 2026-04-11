FROM mcr.microsoft.com/playwright/python:v1.43.0-jammy

# 🔥 FORCE REBUILD (IMPORTANT)
RUN echo "FORCE REBUILD 123"

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:10000"]