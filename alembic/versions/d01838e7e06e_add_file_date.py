"""add file date

Revision ID: d01838e7e06e
Revises: 808e92abac62
Create Date: 2023-07-02 16:54:18.024234

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd01838e7e06e'
down_revision = '808e92abac62'
branch_labels = None
depends_on = None


def upgrade():
    conn = op.get_bind()
    conn.execute(sa.text("ALTER TABLE files ADD COLUMN file_date DATETIME"))


def downgrade():
    conn = op.get_bind()
    conn.execute(sa.text("ALTER TABLE files DROP COLUMN file_date"))
