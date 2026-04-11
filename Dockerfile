FROM mcr.microsoft.com/playwright/python:v1.43.0-jammy

WORKDIR /app

# 🔥 FORCE rebuild every time
ADD requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

ADD . /app

CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:10000"]