import os

import requests
from googleapiclient.discovery import build


class CollectImage():
    def __init__(self, api_key, cse_id):
        self.api_key = api_key
        self.cse_id = cse_id
        self.output_dir = 'output'

    def serch_image(self, search_word, page_limit, image_num):
        """指定したワードでserch apiを叩き、responceのリストを返す

        Args:
            search_word ([type]): 検索ワード
            page_limit ([type]): 何ページ取得するか
            image_num ([type]): 

        Returns:
            [type]: [description]
        """

        service = build("customsearch", "v1", developerKey=self.api_key)
        start_index = 1
        response_list = []

        for n_page in range(0, page_limit):
            try:
                response_list.append(service.cse().list(
                    q=search_word, 
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
        for one_res in range(len(responce_list)):
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
    
    def collect_image(self, search_word, page_limit=10, image_num=10):
        """指定したワードをもとに画像を収集する 全体の実行関数

        Args:
            search_word ([type]): [description]
            page_limit (int, optional): [description]. Defaults to 10.
            image_num (int, optional): [description]. Defaults to 10.

        Returns:
            [type]: [description]
        """

        # search api実行
        response_list = self.serch_image(
            search_word=search_word,
            page_limit=page_limit,
            image_num=image_num,
            )
        
        # 画像urlに変換
        url_list = self.make_url_from_responce(responce_list=response_list)

        # urlから画像を保存
        for i in range(len(url_list)):
            # 拡張子を取得
            extension = os.path.splitext(url_list[i].split("?")[0])[-1]    

            # 出力先を決める
            output_path = os.path.join(self.output_dir, f"{search_word}_{str(i)}{extension}")

            # ダウンロードする
            try:
                self.download_file(url_list[i], output_path=output_path)
            except:
                print("保存に失敗しました ", url_list[i])
        
        return None


