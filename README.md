# google_search_api_image
Googleの[Custom Search JSON API](https://developers.google.com/custom-search/v1/overview?hl=ja)を使って画像を収集します。無料枠を超えた場合課金が発生しますので、公式サイトで料金を確認の上ご利用ください。

## 事前準備
[こちらの記事](https://qiita.com/ysdyt/items/02a9e6b4e70f26385abc) を参考にして必要な情報の収集をお願いします
- Custom Search API のAPIkeyを取得
- 「カスタム検索エンジン」を作成しIDを取得

取得したkeyとidで、`config/api_keys.yaml`内のgoogle_api_key、google_cse_idの値を置き換えてください
```yaml
google_api_key: XXXXX # Custom Search API のAPIkey
google_cse_id: XXXXXX # 「カスタム検索エンジン」のID
```


## 環境構築

[pipenv](https://github.com/pypa/pipenv) で環境を作成します。pipenv の使い方は[公式ドキュメント](https://pipenv-ja.readthedocs.io/ja/translate-ja/)を参照してください。

```shell
pip install pipenv
pipenv install --dev
```

## 実行
`config/search.yaml`に検索したいワードや取得枚数を入力してください。例えばpage_limitを20、image_numを10にした場合、最大200枚取得できます。
```yaml
search_word: 東京 住宅街 # 検索ワード
page_limit: 3 # 何ページ取得するか
image_num: 10 # 最大10
```
run.pyを実行します

```shell
python run.py
```

保存した画像は`output`配下に格納されます