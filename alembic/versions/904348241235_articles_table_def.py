"""articles table def

Revision ID: 904348241235
Revises: 2ce6d93ab5fa
Create Date: 2025-09-18 16:40:24.831816

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from pgvector.sqlalchemy import Vector


# revision identifiers, used by Alembic.
revision: str = '904348241235'
down_revision: Union[str, Sequence[str], None] = '2ce6d93ab5fa'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None



TABLE = "articles"
IDXNAME = "articles_seq_idx"
IDXNAME_SEC = "articles_seq_fk_idx"
IDXNAME_THR = "articles_embedding_seq_idx"

def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        TABLE,
        sa.Column(
            "id", sa.BigInteger,
            nullable=False, primary_key=True,
            autoincrement=True
        ),
        sa.Column(
            "title", sa.String(60), nullable=False
        ),
        sa.Column(
            "content", sa.Text, nullable=False
        ),
        sa.Column(
            "author_id",
            sa.BigInteger, sa.ForeignKey("authors.id"),
            nullable=True
        ),
        sa.Column(
            "category_id",
            sa.BigInteger, sa.ForeignKey("categories.id"),
            nullable=True
        ),
        sa.Column("publish_date", sa.DateTime(timezone=True), nullable=False),
        sa.Column("date_updated", sa.DateTime(timezone=True), nullable=True),
        sa.Column("embedding", Vector(dim=1536))

    )
    op.create_index(IDXNAME, TABLE, ["id", "title"], if_not_exists=True)
    op.create_index(IDXNAME_SEC, TABLE, ["id", "author_id", "category_id"], if_not_exists=True)




def downgrade() -> None:
    """Downgrade schema."""

    op.drop_index(IDXNAME, TABLE, if_exists=True)
    op.drop_index(IDXNAME_SEC, TABLE, if_exists=True)
    op.drop_table(TABLE, if_exists=True)