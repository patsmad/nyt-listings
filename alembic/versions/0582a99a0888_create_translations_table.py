"""create translations table

Revision ID: 0582a99a0888
Revises: 
Create Date: 2023-05-13 12:15:42.049919

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0582a99a0888'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    conn = op.get_bind()
    query = """
    CREATE TABLE items(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        filename VARCHAR(50) NOT NULL,
        x INTEGER NOT NULL,
        y INTEGER NOT NULL,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
    );
    """
    conn.execute(sa.text(query))


def downgrade():
    conn = op.get_bind()
    query = """
    DROP TABLE items;
    """
    conn.execute(query)
