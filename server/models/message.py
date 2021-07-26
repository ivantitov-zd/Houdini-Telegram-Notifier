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

from typing import Optional

from pydantic import BaseModel


class MessageBase(BaseModel):
    chat_id: str
    text: str

    disable_web_page_preview: Optional[bool] = False
    disable_notification: Optional[bool] = False
    parse_mode: Optional[str]


class IncomingMessage(MessageBase):
    custom_bot_api_token: Optional[str]


class OutgoingMessage(MessageBase):
    pass
