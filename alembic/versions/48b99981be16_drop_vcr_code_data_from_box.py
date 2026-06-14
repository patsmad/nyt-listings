"""drop vcr code data from box

Revision ID: 48b99981be16
Revises: d0945dd41a92
Create Date: 2026-06-14 12:19:57.251236

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '48b99981be16'
down_revision = 'd0945dd41a92'
branch_labels = None
depends_on = None


def upgrade():
    conn = op.get_bind()
    conn.execute(sa.text("ALTER TABLE boxes DROP COLUMN channel"))
    conn.execute(sa.text("ALTER TABLE boxes DROP COLUMN time"))
    conn.execute(sa.text("ALTER TABLE boxes DROP COLUMN duration_minutes"))
    conn.execute(sa.text("ALTER TABLE boxes DROP COLUMN vcr_code"))


def downgrade():
    conn = op.get_bind()
    conn.execute(sa.text("ALTER TABLE boxes ADD COLUMN channel VARCHAR(10)"))
    conn.execute(sa.text("ALTER TABLE boxes ADD COLUMN time DATETIME"))
    conn.execute(sa.text("ALTER TABLE boxes ADD COLUMN duration_minutes INTEGER"))
    conn.execute(sa.text("ALTER TABLE boxes ADD COLUMN vcr_code INTEGER"))
