"""Add rating votes to link_info table

Revision ID: 808e92abac62
Revises: 561733f6ef29
Create Date: 2023-05-29 17:36:41.905841

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '808e92abac62'
down_revision = '561733f6ef29'
branch_labels = None
depends_on = None


def upgrade():
    conn = op.get_bind()
    conn.execute(sa.text("ALTER TABLE link_info ADD COLUMN rating REAL NOT NULL DEFAULT 0.0"))
    conn.execute(sa.text("ALTER TABLE link_info ADD COLUMN votes INTEGER NOT NULL DEFAULT 0"))


def downgrade():
    conn = op.get_bind()
    conn.execute(sa.text("ALTER TABLE link_info DROP COLUMN rating"))
    conn.execute(sa.text("ALTER TABLE link_info DROP COLUMN votes"))
