import asyncio
import logging
import re
from datetime import datetime

from telethon import TelegramClient
from telethon.sessions import StringSession
from telethon.tl.types import Message

_LOGGER = logging.getLogger(__name__)


def handle_message(message: Message):
    """Handle the received message and return parsed data."""
    meter_blocks = message.message.split('\n\n')
    meters = []

    for block in meter_blocks:
        lines = block.split('\n')

        if 'Вода' not in lines[0]:
            continue

        match_value = re.search(r'(\d+\.?\d*)', lines[4])
        match_datetime = re.search(r'(\d+\.\d+\.\d+ \d+:\d+)', lines[6])

        meters.append({
            'type': 'hot' if '(Горячая)' in lines[0] else 'cold',
            'mac': lines[2],
            'status': 'online' if 'В сети' in lines[3] else ('warning' if 'Предупреждение' in lines[3] else 'unknown'),
            'value': float(match_value.group(1)) if match_value else 0.0,
            'location': lines[5].replace('🏡', '').strip(),
            'datetime': datetime.strptime(match_datetime.group(1), '%d.%m.%Y %H:%M') if match_datetime else None,
        })

    return meters


async def get_data(api_id: int, api_hash: str, session: str = None):
    """Get parsed water consumption data."""
    bot_name = "@MyIotansBot"

    async with TelegramClient(StringSession(session), api_id, api_hash) as client:
        if session is None:
            print("Session:", client.session.save())

        meters_message: Message | None
        sent_message: Message = await client.send_message(bot_name, "🎛️ Мои счётчики")
        _LOGGER.debug(sent_message)

        meters_message: Message | None = None

        for i in range(30):
            meters_message = (await client.get_messages(bot_name, 1))[0]
            if meters_message.id != sent_message.id:
                break

            meters_message = None
            await asyncio.sleep(2)

        message_ids_to_delete = [sent_message.id]
        if meters_message is not None:
            message_ids_to_delete.append(meters_message.id)

        await client.delete_messages(bot_name, message_ids_to_delete)

    if meters_message is None:
        _LOGGER.warning("No response message received from bot after 60 seconds")
        return []

    data = handle_message(meters_message)
    _LOGGER.debug(data)

    return data