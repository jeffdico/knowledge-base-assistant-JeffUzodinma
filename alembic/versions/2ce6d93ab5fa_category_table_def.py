"""category table def

Revision ID: 2ce6d93ab5fa
Revises: 24fcfec052d5
Create Date: 2025-09-18 16:40:10.002725

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2ce6d93ab5fa'
down_revision: Union[str, Sequence[str], None] = '24fcfec052d5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

TABLE = "categories"
IDXNAME = "category_seq_idx"

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
            "name", sa.String(60), nullable=False
        ),
        sa.Column("date_created", sa.DateTime(timezone=True), nullable=False),
        sa.Column("date_updated", sa.DateTime(timezone=True), nullable=True)
    )
    op.create_index(IDXNAME, TABLE, ["id", "name"], if_not_exists=True)


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index(IDXNAME, TABLE, if_exists=True)
    op.drop_table(TABLE, if_exists=True)

