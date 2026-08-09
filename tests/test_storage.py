from unittest.mock import AsyncMock

import pytest

from src.storage.xhs._store_impl import XhsCsvStoreImplement, XhsJsonStoreImplement
from src.storage.zhihu._store_impl import ZhihuMongoStoreImplement


@pytest.mark.asyncio
async def test_zhihu_mongodb_content_uses_content_id():
    store = ZhihuMongoStoreImplement()
    store.mongo_store.save_or_update = AsyncMock(return_value=True)

    await store.store_content({"content_id": "answer-123", "title": "example"})

    store.mongo_store.save_or_update.assert_awaited_once_with(
        collection_suffix="contents",
        query={"content_id": "answer-123"},
        data={"content_id": "answer-123", "title": "example"},
    )


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("store_class", "writer_method"),
    [
        (XhsCsvStoreImplement, "write_to_csv"),
        (XhsJsonStoreImplement, "write_single_item_to_json"),
    ],
)
async def test_xhs_creator_file_storage_is_not_silently_dropped(store_class, writer_method):
    store = store_class()
    writer = AsyncMock()
    store.writer = writer
    creator = {"user_id": "creator-123"}

    await store.store_creator(creator)

    getattr(writer, writer_method).assert_awaited_once_with(item_type="creators", item=creator)
