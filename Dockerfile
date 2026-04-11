FROM python:3.10-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    wget curl unzip \
    libnss3 libatk1.0-0 libatk-bridge2.0-0 libcups2 \
    libdrm2 libxkbcommon0 libxcomposite1 libxrandr2 \
    libgbm1 libasound2 libxshmfence1 libglib2.0-0 libgtk-3-0 \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# 🔥 FORCE CLEAN INSTALL (NO CACHE)
RUN rm -rf /root/.cache/ms-playwright

# 🔥 INSTALL BROWSERS
RUN python -m playwright install chromium

# 🔥 VERIFY INSTALL (THIS IS KEY)
RUN ls -R /root/.cache/ms-playwright

COPY . .

CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:10000"]