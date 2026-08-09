import config
import pytest
from typer import BadParameter

from src.core.arg import PlatformEnum, parse_cmd


@pytest.fixture
def restore_config():
    names = [
        "PLATFORM",
        "LOGIN_TYPE",
        "CRAWLER_TYPE",
        "START_PAGE",
        "KEYWORDS",
        "ENABLE_GET_COMMENTS",
        "ENABLE_GET_SUB_COMMENTS",
        "HEADLESS",
        "CDP_HEADLESS",
        "ENABLE_IP_PROXY",
        "ENABLE_CDP_MODE",
        "SAVE_DATA_OPTION",
        "COOKIES",
        "CRAWLER_MAX_NOTES_COUNT",
        "XHS_SPECIFIED_NOTE_URL_LIST",
        "XHS_CREATOR_ID_LIST",
        "ZHIHU_SPECIFIED_ID_LIST",
        "ZHIHU_CREATOR_URL_LIST",
    ]
    original = {name: getattr(config, name) for name in names}
    yield
    for name, value in original.items():
        setattr(config, name, value)


def test_only_implemented_platforms_are_exposed():
    assert {platform.value for platform in PlatformEnum} == {"xhs", "zhihu"}


@pytest.mark.asyncio
async def test_zhihu_ids_and_page_limit_are_mapped_to_config(restore_config):
    args = await parse_cmd(
        [
            "--platform",
            "zhihu",
            "--specified_id",
            "https://www.zhihu.com/question/1/answer/2,https://zhuanlan.zhihu.com/p/3",
            "--creator_id",
            "https://www.zhihu.com/people/example",
            "--max_page",
            "3",
            "--enable_proxy",
            "true",
            "--enable_cdp",
            "false",
        ]
    )

    assert args.max_page == 3
    assert config.CRAWLER_MAX_NOTES_COUNT == 60
    assert args.enable_proxy is True
    assert args.enable_cdp is False
    assert config.ENABLE_IP_PROXY is True
    assert config.ENABLE_CDP_MODE is False
    assert config.ZHIHU_SPECIFIED_ID_LIST == [
        "https://www.zhihu.com/question/1/answer/2",
        "https://zhuanlan.zhihu.com/p/3",
    ]
    assert config.ZHIHU_CREATOR_URL_LIST == ["https://www.zhihu.com/people/example"]


@pytest.mark.asyncio
async def test_xhs_ids_are_mapped_to_config(restore_config):
    await parse_cmd(
        [
            "--platform",
            "xhs",
            "--specified_id",
            "note-url",
            "--creator_id",
            "creator-url",
        ]
    )

    assert config.XHS_SPECIFIED_NOTE_URL_LIST == ["note-url"]
    assert config.XHS_CREATOR_ID_LIST == ["creator-url"]


@pytest.mark.asyncio
async def test_start_page_must_be_positive(restore_config):
    with pytest.raises((BadParameter, SystemExit)):
        await parse_cmd(["--start", "0"])
