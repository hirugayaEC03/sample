import streamlit as st
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import requests
import os
import concurrent.futures

def set_chrome_options():
    chrome_options = Options()
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-software-rasterizer")
    chrome_options.binary_location = "/usr/bin/google-chrome"
    return chrome_options

def initialize_driver():
    try:
        service = Service(ChromeDriverManager(version="114.0.5735.90").install(), log_path="chromedriver.log")
        chrome_options = set_chrome_options()
        driver = webdriver.Chrome(service=service, options=chrome_options)
        return driver
    except Exception as e:
        st.error(f"WebDriverの初期化中にエラーが発生しました: {e}")
        return None

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
        st.error(f"エラーが発生しました: {e}")
        if driver:
            driver.quit()
        return []

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
        else:
            st.warning("画像が見つかりませんでした。")





