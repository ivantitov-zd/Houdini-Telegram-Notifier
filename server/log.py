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

import asyncio
import logging
from logging.handlers import QueueHandler, QueueListener
from queue import Queue

from .models import OutgoingMessage
from .services import TelegramBot
from .settings import settings


class TelegramHandler(logging.Handler):
    def __init__(self, api_token, chat_id):
        super(TelegramHandler, self).__init__()
        self._bot = TelegramBot(api_token)
        self._chat_id = chat_id

    def emit(self, record):
        message = OutgoingMessage(
            chat_id=self._chat_id,
            text=self.format(record),
            disable_notification=record.levelno != logging.CRITICAL,
            parse_mode='HTML'
        )
        try:
            asyncio.run(self._bot.send_message(message))
        except RuntimeError:
            pass


def configure_logging():
    root_logger = logging.getLogger('server')
    root_logger.setLevel(logging.INFO)

    formatter = logging.Formatter(
        '<b>Level</b> %(levelname)s\n'
        '<b>Message</b> %(message)s\n'
    )

    telegram_handler = TelegramHandler(settings.bot_api_token, settings.log_chat_id)
    telegram_handler.setLevel(logging.INFO)
    telegram_handler.setFormatter(formatter)
    root_logger.addHandler(telegram_handler)

    log_queue = Queue()
    queue_handler = logging.handlers.QueueHandler(log_queue)
    root_logger.addHandler(queue_handler)

    queue_listener = QueueListener(log_queue, *root_logger.handlers)
    root_logger.handlers = [queue_handler]
    queue_listener.start()
