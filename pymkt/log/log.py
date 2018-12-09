import json
import logging
import platform
import re
import socket
import sys
from collections import OrderedDict
from logging.handlers import SysLogHandler


DEFAULT_FORMAT = '%(asctime)s|%(levelname)s|%(name)s|%(message)s'
DEFAULT_DATE_FORMAT = '%Y-%m-%dT%H:%M:%SZ'


_root = None
_root_name = 'root'


def setup(root_name='root', level='debug',
          fmt=None, date_fmt=None, use_json_format=True,
          stdout_enabled=True,
          syslog_enabled=False,
          syslog_address=('127.0.0.1', 514),
          syslog_facility=SysLogHandler.LOG_LOCAL0,
          syslog_socktype=socket.SOCK_STREAM):
    global _root
    global _root_name
    _root_name = root_name

    level = level.upper()
    fmt = fmt or DEFAULT_FORMAT
    date_fmt = date_fmt or DEFAULT_DATE_FORMAT

    if use_json_format:
        formatter = JsonFormatter(fmt, date_fmt)
    else:
        formatter = logging.Formatter(fmt, date_fmt)

    _root = logging.getLogger(root_name)
    _root.propagate = 0
    _root.setLevel(level)
    _root.handlers.clear()

    if stdout_enabled:
        stream_handler = logging.StreamHandler(stream=sys.stdout)
        stream_handler.setLevel(level)
        stream_handler.setFormatter(formatter)
        _root.addHandler(stream_handler)

    if syslog_enabled:
        syslog_handler = SysLogHandler(
            address=syslog_address,
            facility=syslog_facility,
            socktype=syslog_socktype
        )
        syslog_handler.setLevel(level)
        syslog_handler.setFormatter(formatter)
        _root.addHandler(syslog_handler)


def get_logger(name=None):
    global _root

    if not _root:
        setup(use_json_format=True, stdout_enabled=True, syslog_enabled=False)

    if not name:
        return _root

    return _root.getChild(name)


class ExtentedLogRecord(logging.LogRecord):

    def __init__(self, *args, **kwargs):
        super(ExtentedLogRecord, self).__init__(*args, **kwargs)
        self.hostname = platform.node().split('.', 1)[0]


class JsonFormatter(logging.Formatter):

    def __init__(self, fmt, datefmt):
        self.datefmt = datefmt

        self._fields = self._parse_fields(fmt)

    def _parse_fields(self, s):
        return re.findall(r'%\((.*?)\)s', s)

    def format(self, record):
        record.message = record.getMessage()
        if 'asctime' in self._fields:
            record.asctime = self.formatTime(record, self.datefmt)

        log_record = OrderedDict()
        for field in self._fields:
            log_record[field] = getattr(record, field)

        if record.exc_info:
            if not record.exc_text:
                record.exc_text = self.formatException(record.exc_info)
        if record.exc_text:
            log_record['exc_info'] = record.exc_text
        if record.stack_info:
            log_record['stack_info'] = self.formatStack(record.stack_info)
        return json.dumps(log_record, ensure_ascii=False)


logging.setLogRecordFactory(ExtentedLogRecord)
