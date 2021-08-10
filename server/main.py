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

import aiogram
from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from .log import configure_logging
from .models import IncomingMessage, OutgoingMessage, Status
from .services import telegram

logger = logging.getLogger(__name__)

app = FastAPI(
    title='Houdini Telegram Notifier',
    description='Stateless proxy server for Telegram Bot',
    version='1.0.1'
)


@app.on_event('startup')
async def startup_event():
    configure_logging()
    logger.info('Server started.')


@app.on_event('shutdown')
async def shutdown_event():
    await telegram.default_bot.close()
    logger.info('Server stopped.')


@app.get('/')
async def root():
    return RedirectResponse('https://github.com/anvdev/Houdini-Telegram-Notifier')


@app.post('/api/v1/sendMessage', response_model=Status)
async def send_message(message: IncomingMessage):
    out_message = OutgoingMessage.parse_obj(message)
    if message.custom_bot_api_token:
        custom_bot = aiogram.Bot(message.custom_bot_api_token)
        await telegram.send_message(out_message, custom_bot)
        await custom_bot.close()
    else:
        await telegram.send_message(out_message)
    return Status()
