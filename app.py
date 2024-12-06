from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import streamlit as st
import os

# Chromeのオプションを設定する関数
def set_chrome_options():
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # ヘッドレスモード
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    return chrome_options

# 画像ダウンロードのメイン処理
def download_images_from_button_tags(url):
    chrome_options = set_chrome_options()

    # ローカル環境に保存された `chromedriver` のパスを指定
    chromedriver_path = r"C:\Users\hirug\.wdm\drivers\chromedriver\win64\131.0.6778.87\chromedriver-win32\chromedriver.exe"

    try:
        # 明示的にパスを指定して WebDriver を起動
        driver = webdriver.Chrome(service=Service(chromedriver_path), options=chrome_options)
        driver.get(url)
        st.success("WebDriverの起動に成功しました！")
        # 必要な処理をここに記述
        driver.quit()
    except Exception as e:
        st.error(f"WebDriverの起動に失敗しました: {e}")

# Streamlitアプリケーション
def main():
    st.title("商品画像ダウンロードアプリ (Windows用)")

    url = st.text_input("画像を取得するURLを入力してください:")

    if st.button("画像ダウンロード"):
        if url:
            st.info("画像の取得を開始します...")
            download_images_from_button_tags(url)
        else:
            st.error("URLを入力してください！")

if __name__ == "__main__":
    main()











