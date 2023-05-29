"""Add link_info table

Revision ID: 561733f6ef29
Revises: a0085f601d4d
Create Date: 2023-05-29 14:46:02.032262

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '561733f6ef29'
down_revision = 'a0085f601d4d'
branch_labels = None
depends_on = None


def upgrade():
    conn = op.get_bind()
    query = """
        CREATE TABLE link_info(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            link VARCHAR(100) NOT NULL UNIQUE,
            title VARCHAR(100) NOT NULL,
            year INTEGER NOT NULL,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP);
        """
    conn.execute(sa.text(query))


def downgrade():
    conn = op.get_bind()
    query = """
        DROP TABLE link_info;
        """
    conn.execute(sa.text(query))
