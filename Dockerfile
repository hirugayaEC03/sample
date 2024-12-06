FROM python:3.9-slim

# 必要なライブラリをインストール
RUN apt-get update && apt-get install -y \
    wget \
    unzip \
    curl \
    libnss3 \
    libgconf-2-4 \
    libatk-bridge2.0-0 \
    libgtk-3-0 \
    libgbm-dev \
    libx11-xcb-dev \
    libxcb1 \
    libxcomposite-dev \
    libxcursor-dev \
    libxdamage-dev \
    libxrandr-dev \
    libasound2 \
    fonts-liberation \
    --no-install-recommends && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Chromeのインストール
RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb && \
    apt-get install -y ./google-chrome-stable_current_amd64.deb && \
    rm google-chrome-stable_current_amd64.deb

# Pythonライブラリのインストール
RUN pip install --no-cache-dir streamlit selenium webdriver-manager requests

# 作業ディレクトリの設定
WORKDIR /app

# アプリケーションコードをコピー
COPY . /app

# アプリケーションの実行
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]




