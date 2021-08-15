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

import pyrogram

from ..settings import settings
from ..models import OutgoingMessage

main_client = pyrogram.Client(
    session_name=':memory:',
    api_id=settings.telegram_api_id,
    api_hash=settings.telegram_api_hash,
    app_version='1.1',
    bot_token=settings.telegram_bot_token
)


async def send_message(
        message: OutgoingMessage,
        client: pyrogram.Client = main_client
):
    # Todo: Split large message into multiple messages
    return await client.send_message(**message.dict(exclude_unset=True, exclude_defaults=True))
