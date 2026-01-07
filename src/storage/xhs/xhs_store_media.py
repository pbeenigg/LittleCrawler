# -*- coding: utf-8 -*-
# @Desc    : Xiaohongshu media storage
import pathlib
from typing import Dict

import aiofiles

from src.core.base_crawler import AbstractStoreImage, AbstractStoreVideo
from src.utils import utils


class XiaoHongShuImage(AbstractStoreImage):
    image_store_path: str = "data/xhs/images"

    async def store_image(self, image_content_item: Dict):
        """
        store content

        Args:
            image_content_item:

        Returns:

        """
        await self.save_image(image_content_item.get("notice_id"), image_content_item.get("pic_content"), image_content_item.get("extension_file_name"))

    def make_save_file_name(self, notice_id: str, extension_file_name: str) -> str:
        """
        make save file name by store type

        Args:
            notice_id: notice id
            extension_file_name: image filename with extension

        Returns:

        """
        return f"{self.image_store_path}/{notice_id}/{extension_file_name}"

    async def save_image(self, notice_id: str, pic_content: str, extension_file_name):
        """
        save image to local

        Args:
            notice_id: notice id
            pic_content: image content
            extension_file_name: image filename with extension

        Returns:

        """
        pathlib.Path(self.image_store_path + "/" + notice_id).mkdir(parents=True, exist_ok=True)
        save_file_name = self.make_save_file_name(notice_id, extension_file_name)
        async with aiofiles.open(save_file_name, 'wb') as f:
            await f.write(pic_content)
            utils.logger.info(f"[XiaoHongShuImageStoreImplement.save_image] save image {save_file_name} success ...")


class XiaoHongShuVideo(AbstractStoreVideo):
    video_store_path: str = "data/xhs/videos"

    async def store_video(self, video_content_item: Dict):
        """
        store content

        Args:
            video_content_item:

        Returns:

        """
        await self.save_video(video_content_item.get("notice_id"), video_content_item.get("video_content"), video_content_item.get("extension_file_name"))

    def make_save_file_name(self, notice_id: str, extension_file_name: str) -> str:
        """
        make save file name by store type

        Args:
            notice_id: notice id
            extension_file_name: video filename with extension

        Returns:

        """
        return f"{self.video_store_path}/{notice_id}/{extension_file_name}"

    async def save_video(self, notice_id: str, video_content: str, extension_file_name):
        """
        save video to local

        Args:
            notice_id: notice id
            video_content: video content
            extension_file_name: video filename with extension

        Returns:

        """
        pathlib.Path(self.video_store_path + "/" + notice_id).mkdir(parents=True, exist_ok=True)
        save_file_name = self.make_save_file_name(notice_id, extension_file_name)
        async with aiofiles.open(save_file_name, 'wb') as f:
            await f.write(video_content)
            utils.logger.info(f"[XiaoHongShuVideoStoreImplement.save_video] save video {save_file_name} success ...")
