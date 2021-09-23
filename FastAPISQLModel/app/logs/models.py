from sqlalchemy import Column, Integer, String, TIMESTAMP, PrimaryKeyConstraint
# import sys
#
# sys.path.append("..")
from app.logs.dbconf import Base


# Log Model
class ProcessLog(Base):
    __tablename__ = "api_server_logs"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=True)
    log_level = Column(Integer, nullable=True)
    log_level_name = Column(String, nullable=True)
    method = Column(String, nullable=True)
    args = Column(String, nullable=True)
    module = Column(String, nullable=True)
    func_name = Column(String, nullable=True)
    line_no = Column(String, nullable=True)
    exception_log = Column(String, nullable=True)
    process = Column(Integer, nullable=True)
    thread = Column(String, nullable=True)
    thread_name = Column(String, nullable=True)
    created_timestamp = Column(TIMESTAMP, nullable=True)

    __table_args__ = (
        PrimaryKeyConstraint('id', name='api_server_logs_pkey12'),
        {"schema": "articles", 'extend_existing': True}
    )

    def __repr__(self):
        return f"ProcessLog('{self.name}','{self.log_level}'," \
               f"'{self.log_level_name}'),'{self.fileid}'," \
               f"'{self.args}','{self.module}','{self.func_name}'," \
               f"'{self.line_no}','{self.exception_log}','{self.process}'," \
               f"'{self.thread}','{self.thread_name}'," \
               f"'{self.created_timestamp}')"
