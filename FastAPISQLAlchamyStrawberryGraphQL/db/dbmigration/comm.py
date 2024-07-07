from alembic import op
from sqlalchemy import Column, DateTime, func, text, String, Integer


def create_timestamped_stand_table(table_name, *columns):
    op.create_table(
        table_name,
        *columns,
        Column(
            "created_timestamp",
            DateTime,
            nullable=False,
            server_default=func.current_timestamp(),
        ),
        Column(
            "modified_timestamp",
            DateTime,
            nullable=False,
            server_default=text(
                "CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"),
        ),
        Column(
            "created_by_userid",
            str(50),
            nullable=False
        ),
        Column(
            "modified_by_userid",
            str(50),
            nullable=False
        )
    )


def create_timestamped_table(table_name, *columns):
    op.create_table(
        table_name,
        *columns,
        Column(
            "created_timestamp",
            DateTime,
            nullable=False,
            server_default=func.current_timestamp(),
        ),
        Column(
            "modified_timestamp",
            DateTime,
            nullable=False,
            server_default=text(
                "CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"),
        ),
        Column("deleted_timestamp", DateTime)
    )
