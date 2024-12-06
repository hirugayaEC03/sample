import streamlit as st
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import os
import requests
import concurrent.futures

# Chromeのオプションを設定する関数
def set_chrome_options():
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # ヘッドレスモード
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    return chrome_options

# 複数の画像を並行してダウンロードする関数
def download_images_concurrently(image_urls, save_dir):
    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(lambda url: download_image(url, save_dir), image_urls)

# 画像をダウンロードして保存する関数
def download_image(image_url, save_dir):
    try:
        response = requests.get(image_url, stream=True)
        if response.status_code == 200:
            image_filename = os.path.join(save_dir, os.path.basename(image_url))
            with open(image_filename, "wb") as f:
                for chunk in response.iter_content(1024):
                    f.write(chunk)
        else:
            st.warning(f"画像のダウンロードに失敗しました: {image_url}")
    except Exception as e:
        st.error(f"画像のダウンロード中にエラーが発生しました: {e}")

# メインの画像ダウンロード処理
def download_images_from_button_tags(url):
    chrome_options = set_chrome_options()
    try:
        # 正しい環境のchromedriverを自動的に取得
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    except Exception as e:
        st.error(f"WebDriverの起動に失敗しました: {e}")
        return

    try:
        driver.get(url)
        st.info("ページを読み込み中...")

        # ページに画像があるかを確認
        image_elements = driver.find_elements_by_tag_name("img")
        if not image_elements:
            st.warning("画像が見つかりませんでした。")
            driver.quit()
            return

        # 保存先フォルダを作成
        save_dir = os.path.join(os.getcwd(), "商品画像")
        os.makedirs(save_dir, exist_ok=True)

        # 画像URLを抽出してダウンロード
        image_urls = [img.get_attribute("src") for img in image_elements if img.get_attribute("src")]
        download_images_concurrently(image_urls, save_dir)

        st.success(f"画像のダウンロードが完了しました！保存先: {save_dir}")
    except Exception as e:
        st.error(f"エラーが発生しました: {e}")
    finally:
        driver.quit()

# StreamlitアプリのUI
def main():
    st.title("商品画像ダウンロードアプリ (自動設定)")

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











