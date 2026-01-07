
# -*- coding: utf-8 -*-
from typing import List

import config
from src.core.base_crawler import AbstractStore
from src.models.m_zhihu import ZhihuComment, ZhihuContent, ZhihuCreator
from ._store_impl import (ZhihuCsvStoreImplement,
                                          ZhihuDbStoreImplement,
                                          ZhihuJsonStoreImplement,
                                          ZhihuSqliteStoreImplement,
                                          ZhihuMongoStoreImplement,
                                          ZhihuExcelStoreImplement)
from src.utils import utils
from src.core.var import source_keyword_var


class ZhihuStoreFactory:
    STORES = {
        "csv": ZhihuCsvStoreImplement,
        "db": ZhihuDbStoreImplement,
        "json": ZhihuJsonStoreImplement,
        "sqlite": ZhihuSqliteStoreImplement,
        "mongodb": ZhihuMongoStoreImplement,
        "excel": ZhihuExcelStoreImplement,
    }

    @staticmethod
    def create_store() -> AbstractStore:
        store_class = ZhihuStoreFactory.STORES.get(config.SAVE_DATA_OPTION)
        if not store_class:
            raise ValueError("[ZhihuStoreFactory.create_store] Invalid save option only supported csv or db or json or sqlite or mongodb or excel ...")
        return store_class()

async def batch_update_zhihu_contents(contents: List[ZhihuContent]):
    """
    Batch update Zhihu contents
    Args:
        contents:

    Returns:

    """
    if not contents:
        return

    for content_item in contents:
        await update_zhihu_content(content_item)

async def update_zhihu_content(content_item: ZhihuContent):
    """
    Update Zhihu content
    Args:
        content_item:

    Returns:

    """
    content_item.source_keyword = source_keyword_var.get()
    local_db_item = content_item.model_dump()
    local_db_item.update({"last_modify_ts": utils.get_current_timestamp()})
    utils.logger.info(f"[store.zhihu.update_zhihu_content] zhihu content: {local_db_item}")
    await ZhihuStoreFactory.create_store().store_content(local_db_item)



async def batch_update_zhihu_note_comments(comments: List[ZhihuComment]):
    """
    Batch update Zhihu content comments
    Args:
        comments:

    Returns:

    """
    if not comments:
        return

    for comment_item in comments:
        await update_zhihu_content_comment(comment_item)


async def update_zhihu_content_comment(comment_item: ZhihuComment):
    """
    Update Zhihu content comment
    Args:
        comment_item:

    Returns:

    """
    local_db_item = comment_item.model_dump()
    local_db_item.update({"last_modify_ts": utils.get_current_timestamp()})
    utils.logger.info(f"[store.zhihu.update_zhihu_note_comment] zhihu content comment:{local_db_item}")
    await ZhihuStoreFactory.create_store().store_comment(local_db_item)


async def save_creator(creator: ZhihuCreator):
    """
    Save Zhihu creator information
    Args:
        creator:

    Returns:

    """
    if not creator:
        return
    local_db_item = creator.model_dump()
    local_db_item.update({"last_modify_ts": utils.get_current_timestamp()})
    await ZhihuStoreFactory.create_store().store_creator(local_db_item)
