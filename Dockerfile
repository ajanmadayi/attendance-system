FROM mcr.microsoft.com/playwright/python:v1.58.0-jammy

WORKDIR /app

COPY requirements.txt .

# 🔥 REMOVE playwright from requirements OR ignore reinstall
RUN pip install --no-cache-dir flask gunicorn pandas openpyxl

COPY . .

CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:10000"]