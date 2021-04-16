import logging
from datetime import datetime
from sqlalchemy.exc import SQLAlchemyError
from fastapi.logger import logger as fastapi_logger
from pydantic import BaseModel
import sys

sys.path.append("..")
from db import dbconf_models


class SQLALCHAMYHandler(logging.Handler):
    """
    Logging handler for SqlAlchamy.
    """

    def __init__(self):
        logging.Handler.__init__(self)
        # defining custom log format
        self.LOG_FORMAT = "%(asctime)s:%(msecs)03d %(levelname)s " \
                          "%(filename)s:%(lineno)d %(message)s | "
        # defining the date format for logger
        self.LOG_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

    class ProcessLogModel(BaseModel):
        created_timestamp: datetime
        name: str
        log_level: int
        log_level_name: str
        method: str
        args: str
        module: str
        func_name: str
        line_no: str
        exception_log: str
        process: int
        thread: str
        thread_name: str

    # -------------- Log data ----------------- #
    def insert_log(self, log: ProcessLogModel):
        try:
            db_log = dbconf_models.APILog(
                created_timestamp=log.created_timestamp,
                name=log.name,
                log_level=log.log_level,
                log_level_name=log.log_level_name,
                method=log.method,
                args=log.args,
                module=log.module,
                func_name=log.func_name,
                line_no=log.line_no,
                exception_log=log.exception_log,
                process=log.process,
                thread=log.thread,
                thread_name=log.thread_name)
            db_log.save()
        except SQLAlchemyError as e:
            raise e

    def emit(self, record):
        record.dbtime = datetime.utcfromtimestamp(record.created).strftime(
            "%Y-%m-%d %H:%M:%S")
        f = OneLineExceptionFormatter(self.LOG_FORMAT,
                                      self.LOG_DATE_FORMAT)
        if record.exc_info:
            record.exc_text = f.formatException(record.exc_info)
            # added for fixing quotes causing error
            record.exc_text = record.exc_text.replace("'",
                                                      '"')
        else:
            record.exc_text = ""

        # Insert log record:
        log_data = record.__dict__
        print(log_data)
        log = self.ProcessLogModel(created_timestamp=log_data['dbtime'],
                                   name=str(log_data['name']),
                                   log_level=int(log_data['levelno']),
                                   log_level_name=str(log_data['levelname']),
                                   method=str(log_data['msg']),
                                   args=str(log_data['args']),
                                   module=str(log_data['module']),
                                   func_name=str(log_data['funcName']),
                                   line_no=str(log_data['lineno']),
                                   exception_log=str(log_data['exc_text']),
                                   process=int(log_data['process']),
                                   thread=str(log_data['thread']),
                                   thread_name=str(log_data['threadName']))
        # insert error log in to table
        self.insert_log(log)


# custom log formatter
class OneLineExceptionFormatter(logging.Formatter):
    def formatException(self, exc_info):
        result = super(OneLineExceptionFormatter, self).formatException(
            exc_info)
        return repr(result)  # or format into one line however you want to

    def format(self, record):
        s = super(OneLineExceptionFormatter, self).format(record)
        if record.exc_text:
            s = s.replace('\n', '') + '|'
        return s


# defining log levels
# LOG_LEVEL = logging.ERROR

# Configuring Logs
# db_logger = logging.getLogger()
# db_logger.setLevel(LOG_LEVEL)

# add database handler
handler = SQLALCHAMYHandler()
# db_logger.addHandler(handler)

gunicorn_logger = logging.getLogger("gunicorn.error")
fastapi_logger.setLevel(gunicorn_logger.level)
# add database handler
fastapi_logger.addHandler(handler)
