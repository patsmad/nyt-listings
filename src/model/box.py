from __future__ import annotations
from pydantic import BaseModel
from src.db.model.box import Box as DBBox
from .link import Link
from typing import Optional
from datetime import datetime
from src.analysis.vcr_code import VCRCodeCalculator, ChannelInfo

class Box(BaseModel):
    id: int
    left: int
    top: int
    width: int
    height: int
    channel: Optional[str]
    time: Optional[datetime]
    duration_minutes: Optional[int]
    vcr_code: Optional[int]
    links: list[Link]

    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'left': self.left,
            'top': self.top,
            'width': self.width,
            'height': self.height,
            'channel': self.channel,
            'time': self.time,
            'duration_minutes': self.duration_minutes,
            'vcr_code': self.vcr_code,
            'links': [link.to_dict() for link in self.links]
        }

    @staticmethod
    def from_db(box: DBBox, links: list[Link]) -> Box:
        return Box(**{
            'id': box.id,
            'left': box.left,
            'top': box.top,
            'width': box.width,
            'height': box.height,
            'channel': box.channel,
            'time': box.time,
            'duration_minutes': box.duration_minutes,
            'vcr_code': box.vcr_code,
            'links': links
        })

    def date_in_payload(self, payload: dict) -> bool:
        return 'year' in payload and 'month' in payload and 'day' in payload

    def full_time_in_payload(self, payload: dict) -> bool:
        return self.date_in_payload(payload) and 'hour' in payload and 'minute' in payload

    def update_channel_time_duration(self, payload: dict) -> bool:
        return 'channel' in payload or self.full_time_in_payload(payload) or 'duration' in payload

    def update(self, payload: dict) -> None:
        if 'left' in payload:
            self.left = payload['left']
        if 'top' in payload:
            self.top = payload['top']
        if 'width' in payload:
            self.width = payload['width']
        if 'height' in payload:
            self.height = payload['height']
        if 'vcr_code' in payload and self.date_in_payload(payload):
            channel_info: ChannelInfo = VCRCodeCalculator.from_vcr_code(int(payload['year']), int(payload['month']), int(payload['day']), int(payload['vcr_code']), 0)
            if channel_info is not None:
                self.time = channel_info.time
                self.channel = channel_info.channel
                self.duration_minutes = channel_info.duration_minutes
                self.vcr_code = int(payload['vcr_code'])
        if self.update_channel_time_duration(payload):
            if 'channel' in payload and payload['channel'] in VCRCodeCalculator.channel_to_number:
                self.channel: str = payload['channel']
            if self.full_time_in_payload(payload):
                dt: datetime = datetime(int(payload['year']), int(payload['month']), int(payload['day']), int(payload['hour']), int(payload['minute']))
                self.time: datetime = dt
            if 'duration' in payload:
                self.duration_minutes: int = int(payload['duration'])
            if self.channel is not None and self.time is not None and self.duration_minutes is not None:
                channel_info: ChannelInfo = ChannelInfo(self.channel, self.time, self.duration_minutes)
                self.vcr_code = VCRCodeCalculator.from_channel_info(channel_info)

    @staticmethod
    def get_item_id_to_box_list(boxes: list[DBBox], box_id_to_links: dict[int, list[Link]]) -> dict[int, list[Box]]:
        item_id_to_box_list: dict[int, list[Box]] = {}
        for box in boxes:
            if box.item_id not in item_id_to_box_list:
                item_id_to_box_list[box.item_id] = []
            item_id_to_box_list[box.item_id].append(Box.from_db(box, box_id_to_links.get(box.id, [])))
        return item_id_to_box_list

    def formatted_time(self):
        if self.time is not None:
            return self.time.strftime('%Y-%m-%d %H:%M:00')
