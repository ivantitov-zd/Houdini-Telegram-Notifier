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

import logging


class TelegramHandler(logging.Handler):
    def __init__(self, client, chat_id):
        super(TelegramHandler, self).__init__()
        self._client = client
        self._chat_id = chat_id

    def emit(self, record):
        self._client.send_message(
            chat_id=self._chat_id,
            text=self.format(record),
            disable_notification=record.levelno != logging.CRITICAL
        )
