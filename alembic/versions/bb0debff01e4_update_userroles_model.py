"""update UserRoles model

Revision ID: bb0debff01e4
Revises: 1b51cce0491d
Create Date: 2023-11-18 12:47:29.133748

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'bb0debff01e4'
down_revision: Union[str, None] = '1b51cce0491d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user_permissions', sa.Column('permission_name', sa.String(length=100), nullable=True))
    op.drop_column('user_permissions', 'description')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user_permissions', sa.Column('description', sa.VARCHAR(length=255), autoincrement=False, nullable=True))
    op.drop_column('user_permissions', 'permission_name')
    # ### end Alembic commands ###