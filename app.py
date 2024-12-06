import streamlit as st
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import requests
import os
import concurrent.futures

# Chromeのオプションを設定する関数
def set_chrome_options():
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # ヘッドレスモード
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--ignore-certificate-errors")
    chrome_options.add_argument("--disable-software-rasterizer")  # ソフトウェアラスタライズを無効化
    return chrome_options

# 複数の画像を並行してダウンロードする関数
def download_images_concurrently(image_urls, save_dir):
    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(lambda url: download_image(url, save_dir), image_urls)

# 画像をダウンロードして保存する関数
def download_image(image_url, save_dir):
    try:
        image_response = requests.get(image_url)
        if image_response.status_code == 200:
            image_filename = os.path.join(save_dir, os.path.basename(image_url))
            with open(image_filename, 'wb') as f:
                f.write(image_response.content)
        else:
            st.warning(f"画像のダウンロードに失敗しました: {image_url}")
    except Exception as e:
        st.error(f"画像のダウンロード中にエラーが発生しました: {e}")

# メインの画像ダウンロード処理
def download_images_from_button_tags(url):
    chrome_options = set_chrome_options()

    try:
        # webdriver_managerを使用してChromeDriverを自動的にインストール
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    except Exception as e:
        st.error(f"WebDriverの起動に失敗しました: {e}")
        return

    try:
        driver.get(url)
        st.info("ページを読み込み中...")

        # ページが読み込まれるまで特定の要素が表示されるのを待機
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'o-productdetailvisual_thumb'))
        )

        # 保存先ディレクトリの作成
        save_dir = os.path.join(os.getcwd(), '商品画像')
        os.makedirs(save_dir, exist_ok=True)

        # 画像URLの抽出
        button_tags = driver.find_elements(By.CLASS_NAME, 'o-productdetailvisual_thumb')
        image_urls = []

        if not button_tags:
            st.warning("画像が見つかりませんでした。")
            return

        for button_tag in button_tags:
            image_url = button_tag.get_attribute('data-mainsrc')
            if image_url:
                image_url = 'https:' + image_url if image_url.startswith('//') else image_url
                image_urls.append(image_url)

        driver.quit()

        # 画像を並行してダウンロード
        download_images_concurrently(image_urls, save_dir)
        st.success("画像のダウンロードが完了しました！")
        st.write(f"保存先フォルダ: {save_dir}")
    except Exception as e:
        st.error(f"エラーが発生しました: {e}")
        driver.quit()

# StreamlitアプリのUI
def main():
    st.title("商品画像ダウンロードアプリ (webdriver_manager使用)")

    # URLの入力
    url = st.text_input("画像を取得するURLを入力してください:")

    # ボタンを押してダウンロード処理を開始
    if st.button("画像ダウンロード"):
        if url:
            st.info("画像の取得を開始します...")
            download_images_from_button_tags(url)
        else:
            st.error("URLを入力してください！")

if __name__ == "__main__":
    main()











