from __future__ import annotations
from pydantic import BaseModel
from .file import File
from .link import Link
from .link_info import LinkInfo
from typing import Optional

class LinkFile(BaseModel):
    link_id: int
    confirmed: bool
    file_id: int
    name: str

    def to_dict(self) -> dict:
        return {
            'link_id': self.link_id,
            'confirmed': self.confirmed,
            'file_id': self.file_id,
            'name': self.name
        }

    @staticmethod
    def build(link: Link, link_id_to_file: dict[int, File]) -> LinkFile:
        file = link_id_to_file[link.id]
        return LinkFile(**{
            'link_id': link.id,
            'confirmed': link.confirmed,
            'file_id': file.id,
            'name': file.name
        })

class LinkFiles(BaseModel):
    link: str
    link_info: Optional[LinkInfo]
    link_files: list[LinkFile]

    def to_dict(self) -> dict:
        return {
            'link': self.link,
            'link_info': self.link_info.to_dict() if self.link_info is not None else None,
            'link_files': [link_file.to_dict() for link_file in self.link_files]
        }

    @staticmethod
    def build(link: str, link_info: Optional[LinkInfo], link_files: list[LinkFile]) -> LinkFiles:
        return LinkFiles(**{
            'link': link,
            'link_info': link_info,
            'link_files': link_files
        })
