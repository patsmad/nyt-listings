"""create files table

Revision ID: 7fa351c6daeb
Revises: a0085f601d4d
Create Date: 2023-05-18 08:14:22.457424

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7fa351c6daeb'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    conn = op.get_bind()
    query = """
    CREATE TABLE files(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name VARCHAR(50) NOT NULL UNIQUE,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
        );
    """
    conn.execute(sa.text(query))


def downgrade():
    conn = op.get_bind()
    query = """
    DROP TABLE files;
    """
    conn.execute(sa.text(query))
