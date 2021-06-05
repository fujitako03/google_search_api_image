import os

import requests
from googleapiclient.discovery import build
from tqdm import tqdm


class CollectImage():
    def __init__(self, api_key, cse_id):
        self.api_key = api_key
        self.cse_id = cse_id
        self.output_dir = 'output'

    def serch_image(self, search_query, page_limit, image_num):
        """指定したワードでserch apiを叩き、responceのリストを返す

        Args:
            search_query ([type]): 検索ワード
            page_limit ([type]): 何ページ取得するか
            image_num ([type]): 

        Returns:
            [type]: [description]
        """

        service = build("customsearch", "v1", developerKey=self.api_key)
        start_index = 1
        response_list = []

        print("APIの実行")
        for n_page in range(0, page_limit):
            try:
                response_list.append(service.cse().list(
                    q=search_query, 
                    cx=self.cse_id, 
                    lr='lang_ja', # 検索言語
                    num=image_num, # 1リクエストでいくつの画像を取得するか(Max 10)
                    start=start_index, # ループで取得するためのindex
                    searchType='image' # 画像検索指定
                ).execute())
                start_index = response_list[n_page].get("queries").get("nextPage")[0].get("startIndex")
            except Exception as e:
                print(e)

        return response_list

    
    def make_url_from_responce(self, responce_list):
        """search apiのレスポンスから画像のurlを取得する

        Args:
            responce_list ([type]): [description]

        Returns:
            [type]: [description]
        """
        img_url_list = []
        for one_res in tqdm(range(len(responce_list))):
            if len(responce_list[one_res]['items']) > 0:
                for i in range(len(responce_list[one_res]['items'])):
                    img_url_list.append(responce_list[one_res]['items'][i]['link'])

        return img_url_list
    
    def download_file(self, image_url, output_path):
        """指定したURLの画像をローカルに保存する

        Args:
            image_url ([type]): [description]
            output_path ([type]): [description]

        Returns:
            [type]: [description]
        """
        with open(output_path, mode="wb") as f:
            r = requests.get(image_url)
            f.write(r.content)
        
        return None
    
    def collect_image(self, search_query, page_limit=10, image_num=10):
        """指定したワードをもとに画像を収集する 全体の実行関数

        Args:
            search_query ([type]): [description]
            page_limit (int, optional): [description]. Defaults to 10.
            image_num (int, optional): [description]. Defaults to 10.

        Returns:
            [type]: [description]
        """
        print("\n","="*30)
        print("検索ワード", search_query)

        # search api実行
        response_list = self.serch_image(
            search_query=search_query,
            page_limit=page_limit,
            image_num=image_num,
            )
        
        # 画像urlに変換
        url_list = self.make_url_from_responce(responce_list=response_list)

        # urlから画像を保存
        print("画像のダウンロード")
        failed_url_list = []
        for i in tqdm(range(len(url_list))):
            # 拡張子を取得
            extension = os.path.splitext(url_list[i].split("?")[0])[-1]    

            # 出力先を決める
            output_path = os.path.join(self.output_dir, f"{search_query}_{str(i)}{extension}")

            # ダウンロードする
            try:
                self.download_file(url_list[i], output_path=output_path)
            except:
                failed_url_list.append(url_list[i])
        
        # 保存した枚数
        max_image_num = page_limit * image_num
        failed_image_num = len(failed_url_list)
        success_image_num = max_image_num - failed_image_num
        print(f"{success_image_num}枚/ {max_image_num}枚 の画像が保存に成功しました")

        # 保存に失敗した画像一覧
        if len(failed_url_list) > 0:
            print(f"失敗したURL")
            for error_url in failed_url_list:
                print(error_url)
        
        return None


