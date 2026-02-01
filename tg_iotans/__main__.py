#!/usr/bin/env python3
import argparse
import asyncio
import logging

from . import __version__
from .core import get_data

_LOGGER = logging.getLogger(__name__)


async def main():
    """Main entry point."""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--api-id",
        type=int,
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

    return await get_data(args.api_id, args.api_hash, args.session)


def run():
    asyncio.get_event_loop().run_until_complete(main())


if __name__ == "__main__":
    try:
        run()
    except KeyboardInterrupt:
        pass
