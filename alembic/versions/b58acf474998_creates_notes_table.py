"""creates notes table

Revision ID: b58acf474998
Revises: a5f3c296aea1
Create Date: 2023-07-19 07:07:56.529679

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b58acf474998'
down_revision = 'a5f3c296aea1'
branch_labels = None
depends_on = None


def upgrade():
    conn = op.get_bind()
    query = """
        CREATE TABLE notes(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            box_id INTEGER NOT NULL,
            note varchar(50) NOT NULL,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            CONSTRAINT fk_box
                FOREIGN KEY (box_id)
                REFERENCES boxes(id)
                ON DELETE CASCADE
                );
        """
    conn.execute(sa.text(query))


def downgrade():
    conn = op.get_bind()
    query = """
        DROP TABLE notes;
        """
    conn.execute(sa.text(query))
