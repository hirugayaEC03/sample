FROM python:3.9-slim

# 必要なパッケージをインストール
RUN apt-get update && apt-get install -y \
    chromium-browser \
    chromium-chromedriver \
    libglib2.0-0 \
    libnss3 \
    libgconf-2-4 \
    libfontconfig1 \
    libxrender1 \
    libxext6 \
    libx11-6 \
    libxcomposite1 \
    libxrandr2 \
    libxcursor1 \
    libxdamage1 \
    libxtst6 \
    ca-certificates \
    fonts-liberation \
    libappindicator3-1 \
    libasound2 \
    libnspr4 \
    xdg-utils \
    wget && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# 必要なPythonライブラリをインストール
COPY requirements.txt /app/
RUN pip install -r /app/requirements.txt

# 作業ディレクトリ
WORKDIR /app
