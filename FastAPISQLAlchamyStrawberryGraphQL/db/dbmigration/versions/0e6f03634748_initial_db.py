"""initial db

Revision ID: 0e6f03634748
Revises: 
Create Date: 2023-11-14 14:05:44.506281

"""
from alembic import op
import sqlalchemy as sa
from db.dbmigration.comm import create_timestamped_table

# revision identifiers, used bby Alembic
revision = '0e6f03634748'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    """
    this function creates the following tables in database
    - users
    - user_login_attempt
    - user_articles
    """
    # Create tables
    # op.create_table(
    create_timestamped_table(
        'users',
        sa.Column('id', sa.String(50), primary_key=True),
        sa.Column('first_name', sa.String(50), nullable=False),
        sa.Column('last_name', sa.String(50), nullable=False),
        sa.Column('full_name', sa.String(50), nullable=False),
        sa.Column('gender', sa.String(50), nullable=False),
        sa.Column('email', sa.String(50), unique=True, nullable=False),
        sa.Column('password', sa.String(50), nullable=False),
        sa.Column('photo', sa.String(50), nullable=False),
        sa.Column('city', sa.String(50), nullable=False),
        sa.Column('region', sa.String(50), nullable=False),
        sa.Column('zip', sa.Integer(), nullable=False),
        sa.Column('country', sa.String(50), nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=False),
        sa.Column('is_superuser', sa.Boolean(), nullable=False),
        sa.Column('is_admin', sa.Boolean(), nullable=False),
        sa.Column('created_by_userid', sa.Integer(), nullable=False),
        sa.Column('modified_by_userid', sa.Integer(), nullable=False)
    )

    create_timestamped_table(
        'user_login_attempt',
        sa.Column('id', sa.String(50), primary_key=True),
        sa.Column('email', sa.String(50), nullable=False),
        sa.Column('session_id', sa.String(50), nullable=False),
        sa.Column('ip_address', sa.String(50), nullable=True),
        sa.Column('browser', sa.String(50), nullable=True),
        sa.Column('status', sa.String(50), nullable=False)
    )

    create_timestamped_table(
        'user_articles',
        sa.Column('id', sa.String(50), primary_key=True),
        sa.Column('user_id', sa.String(50), sa.ForeignKey("users.id")),
        sa.Column('article_title', sa.String(50), nullable=False),
        sa.Column('article_text', sa.Text(), nullable=True),
        sa.Column('tags', sa.JSON(), nullable=True)
    )

    # Additional operations, e.g., create indexes or foreign keys


def downgrade():
    """
    this function drop the following tables in database
    - users
    - user_login_attempt
    - user_articles
    """
    # Drop tables
    op.drop_table('user_articles')
    op.drop_table('user_login_attempt')
    op.drop_table('users')
