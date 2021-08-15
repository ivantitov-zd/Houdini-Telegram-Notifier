"""
Houdini-Telegram-Notifier
Copyright (C) 2021 Ivan Titov

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

from enum import Enum
from typing import Optional

from pydantic import BaseModel


class Service(str, Enum):
    Telegram = 'telegram'


class AttachmentType(str, Enum):
    Image = 'image'
    Document = 'document'


class MessageBase(BaseModel):
    chat_id: str
    text: str

    disable_web_page_preview: bool = False
    disable_notification: bool = False
    parse_mode: Optional[str]

    attachment_type: AttachmentType = AttachmentType.Document
    attachment: Optional[str]  # Todo: Base64


class IncomingMessage(MessageBase):
    service: Optional[Service] = Service.Telegram
    custom_bot_api_token: Optional[str]


class OutgoingMessage(MessageBase):
    pass
