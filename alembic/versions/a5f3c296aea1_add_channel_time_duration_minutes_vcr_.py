"""add channel, time, duration_minutes, vcr_code to box

Revision ID: a5f3c296aea1
Revises: d01838e7e06e
Create Date: 2023-07-03 13:37:06.879127

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a5f3c296aea1'
down_revision = 'd01838e7e06e'
branch_labels = None
depends_on = None


def upgrade():
    conn = op.get_bind()
    conn.execute(sa.text("ALTER TABLE boxes ADD COLUMN channel VARCHAR(10)"))
    conn.execute(sa.text("ALTER TABLE boxes ADD COLUMN time DATETIME"))
    conn.execute(sa.text("ALTER TABLE boxes ADD COLUMN duration_minutes INTEGER"))
    conn.execute(sa.text("ALTER TABLE boxes ADD COLUMN vcr_code INTEGER"))


def downgrade():
    conn = op.get_bind()
    conn.execute(sa.text("ALTER TABLE boxes DROP COLUMN channel"))
    conn.execute(sa.text("ALTER TABLE boxes DROP COLUMN time"))
    conn.execute(sa.text("ALTER TABLE boxes DROP COLUMN duration_minutes"))
    conn.execute(sa.text("ALTER TABLE boxes DROP COLUMN vcr_code"))
