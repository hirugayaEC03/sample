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

# Chromeのオプションを設定する関数
def set_chrome_options():
    chrome_options = Options()
    chrome_options.add_argument("--disable-gpu")  # GPUアクセラレーションを無効化
    chrome_options.add_argument("--headless")  # ヘッドレスモード
    chrome_options.add_argument("--no-sandbox")  # サンドボックスを無効化
    chrome_options.add_argument("--disable-dev-shm-usage")  # /dev/shm使用を無効化
    return chrome_options

# 複数の画像を並行してダウンロードする関数
def download_images_concurrently(image_urls, save_dir):
    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(lambda url: download_image(url, save_dir), image_urls)

# 画像をダウンロードして保存する関数
def download_image(image_url, save_dir):
    try:
        image_response = requests.get(image_url, stream=True)
        if image_response.status_code == 200:
            image_filename = os.path.join(save_dir, image_url.split('/')[-1])
            with open(image_filename, 'wb') as f:
                for chunk in image_response.iter_content(1024):
                    f.write(chunk)
        else:
            st.error(f"画像のダウンロードに失敗しました: {image_url}")
    except Exception as e:
        st.error(f"画像のダウンロード中にエラーが発生しました: {e}")

# メインの画像ダウンロード処理
def download_images_from_button_tags(url):
    chrome_options = set_chrome_options()
    service = Service(ChromeDriverManager().install())  # WebDriverManagerで自動インストール
    driver = webdriver.Chrome(service=service, options=chrome_options)

    driver.get(url)

    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'o-productdetailvisual_thumb'))
        )
    except Exception as e:
        st.error(f"ページの読み込みに失敗しました: {e}")
        driver.quit()
        return []

    # 画像URLの抽出
    button_tags = driver.find_elements(By.CLASS_NAME, 'o-productdetailvisual_thumb')
    image_urls = []

    for button_tag in button_tags:
        image_url = button_tag.get_attribute('data-mainsrc')
        if image_url:
            image_url = 'https:' + image_url if image_url.startswith('//') else image_url
            image_urls.append(image_url)

    driver.quit()
    return image_urls

# Streamlit UI
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
            download_images_concurrently(image_urls, save_dir)
            st.success(f"{len(image_urls)}枚の画像を保存しました")
            st.write(f"保存フォルダ: `{save_dir}`")

            # 取得した画像のプレビュー
            st.subheader("取得した画像")
            for img_url in image_urls:
                st.image(img_url, caption=os.path.basename(img_url), use_container_width=True)
        else:
            st.warning("画像が見つかりませんでした。")



