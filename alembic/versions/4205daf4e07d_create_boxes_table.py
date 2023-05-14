"""create boxes table

Revision ID: 4205daf4e07d
Revises: 0582a99a0888
Create Date: 2023-05-14 07:35:56.341739

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4205daf4e07d'
down_revision = '0582a99a0888'
branch_labels = None
depends_on = None


def upgrade():
    conn = op.get_bind()
    query = """
        CREATE TABLE boxes(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            item_id INTEGER NOT NULL,
            left INTEGER NOT NULL,
            top INTEGER NOT NULL,
            width INTEGER NOT NULL,
            height INTEGER NOT NULL,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            CONSTRAINT fk_item
                FOREIGN KEY (item_id)
                REFERENCES items(id)
                ON DELETE CASCADE
                );
        """
    conn.execute(query)


def downgrade():
    conn = op.get_bind()
    query = """
        DROP TABLE boxes;
        """
    conn.execute(query)
