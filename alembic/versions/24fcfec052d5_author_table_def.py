"""author table def

Revision ID: 24fcfec052d5
Revises: 
Create Date: 2025-09-18 16:39:58.922619

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '24fcfec052d5'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


TABLE = "authors"
IDXNAME="authors_seq_idx"

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
            "name",sa.String(60), nullable=False
        ),
        sa.Column(
            "bio", sa.String(300), nullable=True
        ),
        sa.Column("date_created", sa.DateTime(timezone=True), nullable=False),
        sa.Column("date_updated", sa.DateTime(timezone=True))
    )

    op.create_index(IDXNAME, TABLE,["id", "name"], if_not_exists=True)


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index(IDXNAME, TABLE, if_exists=True)
    op.drop_table(TABLE, if_exists=True)

