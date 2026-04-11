FROM mcr.microsoft.com/playwright/python:v1.58.0-jammy

WORKDIR /app

# 🔥 CRITICAL FIX
ENV PLAYWRIGHT_BROWSERS_PATH=/ms-playwright

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

RUN playwright install

COPY . .

CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:10000"]