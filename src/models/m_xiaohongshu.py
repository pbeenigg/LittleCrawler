
# -*- coding: utf-8 -*-


from pydantic import BaseModel, Field


class NoteUrlInfo(BaseModel):
    note_id: str = Field(title="note id")
    xsec_token: str = Field(title="xsec token")
    xsec_source: str = Field(title="xsec source")


class CreatorUrlInfo(BaseModel):
    """Xiaohongshu creator URL information"""
    user_id: str = Field(title="user id (creator id)")
    xsec_token: str = Field(default="", title="xsec token")
    xsec_source: str = Field(default="", title="xsec source")
