"""add file dimensions

Revision ID: d0945dd41a92
Revises: b58acf474998
Create Date: 2025-12-03 21:14:41.654812

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd0945dd41a92'
down_revision = 'b58acf474998'
branch_labels = None
depends_on = None


def upgrade():
    conn = op.get_bind()
    conn.execute(sa.text("ALTER TABLE files ADD COLUMN width INTEGER"))
    conn.execute(sa.text("ALTER TABLE files ADD COLUMN height INTEGER"))


def downgrade():
    conn = op.get_bind()
    conn.execute(sa.text("ALTER TABLE files DROP COLUMN width"))
    conn.execute(sa.text("ALTER TABLE files DROP COLUMN height"))
