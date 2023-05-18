"""create links table

Revision ID: a0085f601d4d
Revises: 4205daf4e07d
Create Date: 2023-05-14 08:59:46.146017

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a0085f601d4d'
down_revision = '4205daf4e07d'
branch_labels = None
depends_on = None


def upgrade():
    conn = op.get_bind()
    query = """
        CREATE TABLE links(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            box_id INTEGER NOT NULL,
            link varchar(50),
            confirmed TINYINT(1) DEFAULT 0 NOT NULL,
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
        DROP TABLE links;
        """
    conn.execute(query)
