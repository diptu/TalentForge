"""drop username column from users

Revision ID: 2a5fa5b29f1c
Revises: 3e759522590d
Create Date: 2025-08-31 21:47:04.433624

"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "2a5fa5b29f1c"
down_revision: Union[str, Sequence[str], None] = "3e759522590d"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Drop the username column
    op.drop_column("users", "username")


def downgrade() -> None:
    # Re-add the username column (nullable to avoid data issues)
    op.add_column("users", sa.Column("username", sa.String(), nullable=True))
