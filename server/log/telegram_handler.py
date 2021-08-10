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

import requests


class TelegramHandler(logging.Handler):
    def __init__(self, api_token, chat_id):
        super(TelegramHandler, self).__init__()
        self._api_token = api_token
        self._chat_id = chat_id
        self._session = requests.Session()

    def emit(self, record):
        url = f'https://api.telegram.org/bot{self._api_token}/sendMessage'
        message = {
            'chat_id': self._chat_id,
            'text': self.format(record),
            'disable_notification': record.levelno != logging.CRITICAL,
            'parse_mode': 'HTML'
        }
        self._session.post(url, json=message, timeout=(3.05, 5))
