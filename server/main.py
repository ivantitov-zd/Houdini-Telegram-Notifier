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

from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from .log import configure_logging
from .routers import api
from .services import telegram

logger = logging.getLogger(__name__)

app = FastAPI(
    title='Houdini Notifier',
    description='Stateless proxy server for Telegram Bot',
    version='1.1'
)

app.include_router(api.router)


@app.on_event('startup')
async def on_startup():
    await telegram.main_client.start()
    configure_logging()
    logger.info('Server started.')


@app.on_event('shutdown')
async def on_shutdown():
    logger.info('Server stopped.')
    await asyncio.sleep(3)
    await telegram.main_client.stop()


@app.get('/', response_class=RedirectResponse)
async def root():
    return RedirectResponse('https://github.com/anvdev/Houdini-Telegram-Notifier')
