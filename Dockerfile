FROM mcr.microsoft.com/playwright/python:v1.58.0-jammy

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# 🔥 INSTALL ALL REQUIRED BROWSERS (CRITICAL)
RUN playwright install

COPY . .

CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:10000"]