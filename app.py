import os
import subprocess
import streamlit as st
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
import concurrent.futures

# 依存関係を確認する関数
def check_dependencies():
    errors = []

    # Check for Chromium
    if not os.path.exists("/usr/bin/chromium-browser"):
        errors.append("Chromium is missing at /usr/bin/chromium-browser")
    else:
        try:
            output = subprocess.check_output(["/usr/bin/chromium-browser", "--version"])
            st.write(f"Chromium version: {output.decode().strip()}")
        except Exception as e:
            errors.append(f"Failed to verify Chromium version: {e}")

    # Check for Chromedriver
    if not os.path.exists("/usr/bin/chromedriver"):
        errors.append("Chromedriver is missing at /usr/bin/chromedriver")
    else:
        try:
            output = subprocess.check_output(["/usr/bin/chromedriver", "--version"])
            st.write(f"Chromedriver version: {output.decode().strip()}")
        except Exception as e:
            errors.append(f"Failed to verify Chromedriver version: {e}")

    return errors

# Chromeのオプションを設定する関数
def set_chrome_options():
    chrome_options = Options()
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.binary_location = "/usr/bin/chromium-browser"  # Chromiumのパスを指定
    return chrome_options

# WebDriverを初期化する関数
def initialize_driver():
    try:
        # aptでインストールされたchromedriverを使用
        service = Service("/usr/bin/chromedriver")
        chrome_options = set_chrome_options()
        driver = webdriver.Chrome(service=service, options=chrome_options)
        return driver
    except Exception as e:
        st.error(f"WebDriverの初期化中にエラーが発生しました: {e}")
        return None

# URLから画像をダウンロードする関数
def download_image(image_url, save_dir):
    try:
        image_response = requests.get(image_url, stream=True)
        if image_response.status_code == 200:
            image_filename = os.path.join(save_dir, image_url.split('/')[-1])
            with open(image_filename, 'wb') as f:
                for chunk in image_response.iter_content(1024):
                    f.write(chunk)
    except Exception as e:
        st.error(f"画像のダウンロード中にエラーが発生しました: {e}")

# ボタンタグから画像URLを取得する関数
def download_images_from_button_tags(url):
    driver = initialize_driver()
    if not driver:
        return []

    try:
        driver.get(url)
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'o-productdetailvisual_thumb'))
        )
        button_tags = driver.find_elements(By.CLASS_NAME, 'o-productdetailvisual_thumb')
        image_urls = [
            'https:' + tag.get_attribute('data-mainsrc') if tag.get_attribute('data-mainsrc').startswith('//') else tag.get_attribute('data-mainsrc')
            for tag in button_tags
        ]
        driver.quit()
        return image_urls
    except Exception as e:
        st.error(f"画像URLの取得中にエラーが発生しました: {e}")
        if driver:
            driver.quit()
        return []

# StreamlitアプリのUI
st.title("Seleniumを使った画像取得アプリ")

# 依存関係の確認セクション
st.header("Dependency Check for Chromium and Chromedriver")
errors = check_dependencies()
if errors:
    for error in errors:
        st.error(error)
else:
    st.success("All dependencies are properly installed.")

# Seleniumを使った画像取得セクション
st.header("Image Scraper")
url = st.text_input("画像を取得するURLを入力してください")
if st.button("画像を取得"):
    if not url:
        st.error("URLを入力してください")
    else:
        st.info("画像を取得中です...")
        image_urls = download_images_from_button_tags(url)

        if image_urls:
            save_dir = "downloaded_images"
            os.makedirs(save_dir, exist_ok=True)
            with concurrent.futures.ThreadPoolExecutor() as executor:
                executor.map(lambda img_url: download_image(img_url, save_dir), image_urls)
            st.success(f"{len(image_urls)}枚の画像を保存しました")
            st.write(f"保存フォルダ: `{save_dir}`")

            # プレビューを表示
            st.subheader("取得した画像")
            for img_url in image_urls:
                st.image(img_url, caption=os.path.basename(img_url), use_container_width=True)
        else:
            st.warning("画像が見つかりませんでした。")










