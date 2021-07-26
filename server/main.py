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

from fastapi import FastAPI

from .log import configure_logging
from .models import IncomingMessage, OutgoingMessage, Status
from .services import TelegramBot
from .settings import settings

logger = logging.getLogger(__name__)

bot = TelegramBot(settings.bot_api_token)

app = FastAPI(
    title='Houdini Telegram Notifier',
    description='Stateless proxy server for Telegram Bot',
    version='1.0.0'
)


@app.on_event('startup')
async def configure():
    configure_logging()


@app.post('/api/v1/sendMessage', response_model=Status)
async def send_message(message: IncomingMessage):
    out_message = OutgoingMessage.parse_obj(message)
    if message.custom_bot_api_token:
        custom_bot = TelegramBot(message.custom_bot_api_token)
        response = await custom_bot.send_message(out_message)
    else:
        response = await bot.send_message(out_message)
    response_data = await response.json()
    return Status(delivered=response_data.get('ok', False))
