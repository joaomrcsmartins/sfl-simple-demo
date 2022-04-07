# pylint: disable=C0111
import logging


def filter_good_logs(record: logging.LogRecord) -> bool:
    return record.levelno == logging.INFO or record.levelno == logging.DEBUG


def filter_bad_logs(record: logging.LogRecord) -> bool:
    return not filter_good_logs(record)


LOG_FORMAT = "%(asctime)s :: %(levelname)s :: Service: %(name)s - %(message)s"
formatter = logging.Formatter(LOG_FORMAT, datefmt='%Y-%m-%d %H:%M:%S')

good_logs_handler = logging.FileHandler(filename="good_logfile.log")
good_logs_handler.setFormatter(formatter)
good_logs_handler.addFilter(filter_good_logs)

bad_logs_handler = logging.FileHandler(filename="bad_logfile.log")
bad_logs_handler.setFormatter(formatter)
bad_logs_handler.addFilter(filter_bad_logs)

logging.getLogger('').setLevel(logging.DEBUG)
logging.getLogger('').addHandler(good_logs_handler)
logging.getLogger('').addHandler(bad_logs_handler)


class RequestAdapter(logging.LoggerAdapter):
    def process(self, msg, kwargs):
        return 'Request ID: {} -> {}'.format(self.extra['request_id'], msg), kwargs


def get_logger(service: str, request_id: str) -> logging.Logger:
    service_logger = logging.getLogger(service)
    adapter = RequestAdapter(service_logger, {'request_id': request_id})
    return adapter
