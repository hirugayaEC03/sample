import streamlit as st
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import os
import stat
import requests
import concurrent.futures

# Chromeのオプションを設定する関数
def set_chrome_options():
    chrome_options = Options()
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--headless")  # ヘッドレスモード
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.binary_location = "/usr/bin/chromium-browser"  # Chromiumのパスを指定
    return chrome_options

# WebDriverを初期化する関数
def initialize_driver():
    try:
        chromedriver_path = ChromeDriverManager().install()
        os.chmod(chromedriver_path, stat.S_IRWXU)  # 実行権限を付与
        service = Service(chromedriver_path)
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







