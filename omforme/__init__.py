import datetime as dti
import logging
import os
import pathlib
from typing import no_type_check

# [[[fill git_describe()]]]
__version__ = '2022.10.2+parent.e8735f64'
# [[[end]]] (checksum: 8ed2e7e93655a22c692ab7fce30e0ec8)
__version_info__ = tuple(
    e if '-' not in e else e.split('-')[0] for part in __version__.split('+') for e in part.split('.') if e != 'parent'
)
__all__: list[str] = []

APP_ALIAS = 'omforme'
APP_ENV = 'OMFORME'
APP_NAME = 'Reshape (Danish: omforme).'
DEBUG = bool(os.getenv(f'{APP_ENV}_DEBUG', ''))
DEFAULT_CONFIG_NAME = '.omforme.json'
DEFAULT_LF_ONLY = 'YES'
ENCODING = 'utf-8'
ENCODING_ERRORS_POLICY = 'ignore'
QUIET = False
VERBOSE = bool(os.getenv(f'{APP_ENV}_VERBOSE', ''))
STRICT = bool(os.getenv(f'{APP_ENV}_STRICT', ''))
log = logging.getLogger()  # Module level logger is sufficient
LOG_FOLDER = pathlib.Path('logs')
LOG_FILE = f'{APP_ALIAS}.log'
LOG_PATH = pathlib.Path(LOG_FOLDER, LOG_FILE) if LOG_FOLDER.is_dir() else pathlib.Path(LOG_FILE)
LOG_LEVEL = logging.INFO

TS_FORMAT_LOG = '%Y-%m-%dT%H:%M:%S'
TS_FORMAT_PAYLOADS = '%Y-%m-%d %H:%M:%S.%f UTC'


@no_type_check
def formatTime_RFC3339(self, record, datefmt=None):  # noqa
    """HACK A DID ACK we could inject .astimezone() to localize ..."""
    return dti.datetime.fromtimestamp(record.created, dti.timezone.utc).isoformat()  # pragma: no cover


@no_type_check
def init_logger(name=None, level=None):
    """Initialize module level logger"""
    global log  # pylint: disable=global-statement

    log_format = {
        'format': '%(asctime)s %(levelname)s [%(name)s]: %(message)s',
        'datefmt': TS_FORMAT_LOG,
        # 'filename': LOG_PATH,
        'level': LOG_LEVEL if level is None else level,
    }
    logging.Formatter.formatTime = formatTime_RFC3339
    logging.basicConfig(**log_format)
    log = logging.getLogger(APP_ENV if name is None else name)
    log.propagate = True


init_logger(name=APP_ENV, level=logging.DEBUG if DEBUG else None)
