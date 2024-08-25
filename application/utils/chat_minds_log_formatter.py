import logging
import time
from flask import request, g


class ChatMindsLogFormatter(logging.Formatter):
    def format(self, record):
        record.url = request.url
        record.remote_addr = request.remote_addr
        try:
            record.response_time = time.time() - g.start
        except:
            record.response_time = 0
        record.request_type = request.method
        record.http_version = request.environ.get('SERVER_PROTOCOL')
        return super().format(record)

