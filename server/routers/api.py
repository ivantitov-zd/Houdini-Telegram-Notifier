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

from fastapi import APIRouter
import pyrogram

from ..models import IncomingMessage, OutgoingMessage, Status
from ..services import telegram

router = APIRouter(prefix='/api')


@router.post('/sendMessage', response_model=Status)
@router.post('/v1/sendMessage', response_model=Status)
async def send_message(message: IncomingMessage):
    out_message = OutgoingMessage.parse_obj(message)
    if message.custom_bot_api_token:
        async with pyrogram.Client(
                session_name=':memory:',
                bot_token=message.custom_bot_api_token
        ) as client:
            await telegram.send_message(out_message, client)
    else:
        await telegram.send_message(out_message)
    return Status().dict(exclude_unset=True)
