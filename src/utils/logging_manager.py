import logging
import sys

_CONFIGURED = False


def get_logger(name: str) -> logging.Logger:
    global _CONFIGURED
    if not _CONFIGURED:
        root = logging.getLogger('resume-machine')
        root.setLevel(logging.DEBUG)
        if not root.handlers:
            handler = logging.StreamHandler(sys.stdout)
            handler.setLevel(logging.DEBUG)
            formatter = logging.Formatter(
                '%(asctime)s [%(name)s] %(levelname)s %(message)s'
            )
            handler.setFormatter(formatter)
            root.addHandler(handler)
        _CONFIGURED = True
    return logging.getLogger(name)


def set_level(level: str) -> None:
    logging.getLogger('resume-machine').setLevel(getattr(logging, level.upper(), logging.INFO))
