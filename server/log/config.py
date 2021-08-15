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
from logging.handlers import QueueHandler, QueueListener
from queue import SimpleQueue as Queue

from ..services import telegram
from ..settings import settings
from .telegram_handler import TelegramHandler


def configure_logging():
    main_logger = logging.getLogger('server')
    main_logger.setLevel(logging.INFO)

    formatter = logging.Formatter(
        '<b>Level</b>: %(levelname)s\n'
        '<b>Logger</b>: %(name)s\n'
        '<b>Message</b>: %(message)s'
    )

    telegram_handler = TelegramHandler(
        client=telegram.main_client,
        chat_id=int(settings.telegram_log_chat_id)
    )
    telegram_handler.setLevel(logging.INFO)
    telegram_handler.setFormatter(formatter)

    log_queue = Queue()
    queue_handler = logging.handlers.QueueHandler(log_queue)
    main_logger.addHandler(queue_handler)

    queue_listener = QueueListener(log_queue, telegram_handler)
    queue_listener.start()
