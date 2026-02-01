"""Telegram client for receiving water consumption data from IotansBot."""
from .core import get_data


def get_version():
    """Get package version with fallback."""
    try:
        from importlib.metadata import version
        return version("tg_iotans")
    except (ImportError, ModuleNotFoundError):
        return '0.0.0'


__version__ = get_version()

__all__ = ['__version__', 'get_version', 'get_data']