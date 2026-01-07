
# 小红书平台配置

# 排序方式，具体的枚举值在 infra/xhs/field.py中
SORT_TYPE = "popularity_descending"

# 指定笔记URL列表, 必须要携带xsec_token参数
XHS_SPECIFIED_NOTE_URL_LIST = [
    "https://www.xiaohongshu.com/explore/64b95d01000000000c034587?xsec_token=AB0EFqJvINCkj6xOCKCQgfNNh8GdnBC_6XecG4QOddo3Q=&xsec_source=pc_cfeed"
    # ........................
]

# 指定创作者URL列表，需要携带xsec_token和xsec_source参数

XHS_CREATOR_ID_LIST = [
    "https://www.xiaohongshu.com/user/profile/5f58bd990000000001003753?xsec_token=ABYVg1evluJZZzpMX-VWzchxQ1qSNVW3r-jOEnKqMcgZw=&xsec_source=pc_search"
    # ........................
]
