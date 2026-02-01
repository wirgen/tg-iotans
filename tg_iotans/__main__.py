#!/usr/bin/env python3
import argparse
import asyncio
import logging
import re
from datetime import datetime

from telethon import TelegramClient
from telethon.sessions import StringSession
from telethon.tl.types import Message

from . import __version__

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


async def get_data(client: TelegramClient):
    """Get parsed water consumption data."""
    bot_name = "@MyIotansBot"

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

    return handle_message(meters_message)


async def main():
    """Main entry point."""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--api-id",
        type=str,
        required=True,
        help="Telegram App Api ID",
    )
    parser.add_argument(
        "--api-hash",
        type=str,
        required=True,
        help="Telegram App Api Hash",
    )
    parser.add_argument(
        "--session",
        type=str,
        help="Session string",
    )
    #
    parser.add_argument("--debug", action="store_true", help="Log DEBUG messages")
    parser.add_argument(
        "--log-format", default=logging.BASIC_FORMAT, help="Format for log messages"
    )
    parser.add_argument(
        "--version",
        action="version",
        version=__version__,
        help="Print version and exit",
    )
    args = parser.parse_args()

    logging.basicConfig(
        level=logging.DEBUG if args.debug else logging.INFO, format=args.log_format
    )
    _LOGGER.debug(args)

    client = TelegramClient(StringSession(args.session), args.api_id, args.api_hash)
    await client.connect()

    if args.session is None:
        print("Session:", client.session.save())

    data = await get_data(client)
    _LOGGER.debug(data)

    return data


def run():
    asyncio.get_event_loop().run_until_complete(main())


if __name__ == "__main__":
    try:
        run()
    except KeyboardInterrupt:
        pass
