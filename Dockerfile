FROM mcr.microsoft.com/playwright/python:v1.43.0-jammy

WORKDIR /app

# 🔥 install dependencies FIRST (important for cache)
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# 🔥 then copy rest of code
COPY . .

CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:10000"]