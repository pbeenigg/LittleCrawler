import pytest
from pydantic import ValidationError

from api.schemas import CrawlerStartRequest, CrawlerTypeEnum, PlatformEnum
from api.services.crawler_manager import CrawlerManager


def test_build_command_passes_supported_web_options_to_cli():
    request = CrawlerStartRequest(
        platform=PlatformEnum.ZHIHU,
        crawler_type=CrawlerTypeEnum.SEARCH,
        keywords="python",
        max_pages=2,
        enable_proxy=True,
        enable_cdp=False,
    )

    command = CrawlerManager()._build_command(request)

    assert command[:4] == ["uv", "run", "python", "main.py"]
    assert command[command.index("--max_page") + 1] == "2"
    assert command[command.index("--keywords") + 1] == "python"
    assert command[command.index("--enable_proxy") + 1] == "true"
    assert command[command.index("--enable_cdp") + 1] == "false"


@pytest.mark.parametrize("max_pages", [0, -1])
def test_crawler_request_rejects_non_positive_page_limit(max_pages):
    with pytest.raises(ValidationError):
        CrawlerStartRequest(platform=PlatformEnum.XHS, keywords="python", max_pages=max_pages)


@pytest.mark.parametrize("start_page", [0, -1])
def test_crawler_request_rejects_non_positive_start_page(start_page):
    with pytest.raises(ValidationError):
        CrawlerStartRequest(platform=PlatformEnum.XHS, keywords="python", start_page=start_page)


@pytest.mark.parametrize(
    ("crawler_type", "field_name"),
    [
        (CrawlerTypeEnum.SEARCH, "keywords"),
        (CrawlerTypeEnum.DETAIL, "specified_ids"),
        (CrawlerTypeEnum.CREATOR, "creator_ids"),
    ],
)
def test_crawler_request_requires_input_for_selected_mode(crawler_type, field_name):
    with pytest.raises(ValidationError, match=field_name):
        CrawlerStartRequest(platform=PlatformEnum.XHS, crawler_type=crawler_type)
