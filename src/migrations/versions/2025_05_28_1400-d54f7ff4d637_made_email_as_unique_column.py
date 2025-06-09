from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "d54f7ff4d637"
down_revision: Union[str, None] = "8738294b133c"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_unique_constraint(None, "users", ["email"])


def downgrade() -> None:
    op.drop_constraint(None, "users", type_="unique")
