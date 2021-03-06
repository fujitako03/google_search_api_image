import os

from omegaconf import OmegaConf

from src.collect_image import CollectImage

# configファイルの読み込み
config_dir = "config"
key_config = OmegaConf.load(os.path.join(config_dir, "api_keys.yaml"))
search_config = OmegaConf.load(os.path.join(config_dir, "search.yaml"))

# インスタンスの初期化
ci = CollectImage(
    api_key=key_config.google_api_key,
    cse_id=key_config.google_cse_id
)

#検索ワード
search_queries = search_config.search_queries

# 実行(outputの下に保存される)
for query in search_queries:
    ci.collect_image(
        search_query=query,
        page_limit=search_config.page_limit,
        image_num=search_config.image_num
        )
