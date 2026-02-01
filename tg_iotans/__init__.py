"""Telegram client for receiving water consumption data from IotansBot."""


def get_version():
    """Get package version with fallback."""
    try:
        from importlib.metadata import version
        return version("tg_iotans")
    except Exception:
        return '0.0.0'


__version__ = get_version()

__all__ = ['__version__', 'get_version']
