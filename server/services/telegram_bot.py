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

import aiohttp

from ..models import OutgoingMessage


class TelegramBot:
    __slots__ = 'api_token', 'session'

    def __init__(self, api_token: str):
        self.api_token = api_token
        self.session = None

    async def send_message(self, message: OutgoingMessage):
        if self.session is None:
            timeout = aiohttp.ClientTimeout(total=60)
            self.session = aiohttp.ClientSession(timeout=timeout)

        url = f'https://api.telegram.org/bot{self.api_token}/sendMessage'
        data = message.dict(exclude_unset=True, exclude_defaults=True)
        response = await self.session.post(url, json=data)
        return response
