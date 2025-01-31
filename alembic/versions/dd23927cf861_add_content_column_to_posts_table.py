"""add content column to posts table

Revision ID: dd23927cf861
Revises: 44e56c0b8dbb
Create Date: 2025-01-30 18:18:50.707158

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'dd23927cf861'
down_revision: Union[str, None] = '44e56c0b8dbb'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'content')
    pass
