import requests
import os
import time
from tqdm import tqdm


def crawl_unsplash(
        unsplash_key: str,
        query: str = "pattern", num_photos: int = 1000, per_page: int = 30):
    """
    Unsplashから画像をクローリングする関数．
    指定したクエリに関連する画像を取得する．num_photosで指定した枚数の画像を取得するが，あくまで最大数設定であり，実際に取得できる枚数はその限りではない．
    また，1クロールで1ページのクロールを行い，1ページあたり最大30枚の画像を取得し，1クロールごとに90秒の待機時間がある．

    Parameters
    ----------
    unsplash_key : str
        Unsplash APIのアクセスキー
    query : str
        検索クエリ
    num_photos : int
        クローリングする画像の枚数
    per_page : int
        1ページあたりの画像数, 最大30枚

    Returns
    -------
    None
    """
    
    # パラメータのチェック
    if unsplash_key is None:
        raise ValueError("Unsplash API key is required.")
    if isinstance(query, str) is False:
        raise ValueError("query must be a string.")
    if isinstance(num_photos, int) is False:
        raise ValueError("num_photos must be an integer.")
    if isinstance(per_page, int) is False:
        raise ValueError("per_page must be an integer.")

    pages = num_photos // per_page  # → ページ分だけリクエストすることになる

    for current_page in tqdm(range(pages)):
        # APIエンドポイント
        url = "https://api.unsplash.com/search/photos"

        # APIリクエストを送信
        response = requests.get(url, params={
                "client_id": unsplash_key,
                "query": query,
                "page": current_page,
                "per_page": per_page
            })

        # ステータスコードが200以外の場合はエラー
        if response.status_code != 200:
            print(f"Error: {response.status_code}")
            continue

        # レスポンスのJSONデータを取得
        data = response.json()

        # 最大ページ数に達したら終了
        total_pages = data["total_pages"]
        if current_page >= total_pages:
            Warning("No more pages.")
            break

        # ページ番号を3桁にしてファイル名にする
        current_page = str(current_page).zfill(3)
        # レスポンスを保存するためのディレクトリを作成
        save_dir = f"./data/json/{query}"
        os.makedirs(save_dir, exist_ok=True)
        with open(f"{save_dir}/page_{current_page}.json", "w") as f:
            f.write(str(data))

        # 画像を保存するためのディレクトリを作成
        save_dir = f"./data/images/{query}"
        os.makedirs(save_dir, exist_ok=True)

        # 画像のURLを取得
        if "results" in data:
            for result in data["results"]:
                
                # 画像のURLを取得
                image_url = result["urls"]["regular"]
                
                # 画像データを取得
                image_data = requests.get(image_url).content
                
                # 保存する画像のファイル名
                image_name = result["slug"] + ".jpg"
                image_path = os.path.join(save_dir, image_name)
                # 画像として書き出し
                with open(f"{image_path}", "wb") as handler:
                    handler.write(image_data)
        else:
            # print("No results found.")
            pass

        time.sleep(90)  # 90秒待機


if __name__ == "__main__":
    # Unsplash APIのアクセスキー
    unsplash_key = os.getenv("UNSPLASH_KEY")
    query = "pattern"
    crawl_unsplash(
        unsplash_key, 
        query=query, num_photos=1000, per_page=30
        )
