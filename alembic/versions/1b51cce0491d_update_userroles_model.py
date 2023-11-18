"""update UserRoles model

Revision ID: 1b51cce0491d
Revises: 31ab0356ca77
Create Date: 2023-11-18 00:22:15.761882

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1b51cce0491d'
down_revision: Union[str, None] = '31ab0356ca77'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user_roles', sa.Column('role_name', sa.String(length=50), nullable=True))
    op.add_column('user_roles', sa.Column('created_at', sa.DateTime(), nullable=False))
    op.add_column('user_roles', sa.Column('updated_at', sa.DateTime(), nullable=False))
    op.create_unique_constraint(None, 'user_roles', ['role_name'])
    op.drop_column('user_roles', 'description')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user_roles', sa.Column('description', sa.VARCHAR(length=255), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'user_roles', type_='unique')
    op.drop_column('user_roles', 'updated_at')
    op.drop_column('user_roles', 'created_at')
    op.drop_column('user_roles', 'role_name')
    # ### end Alembic commands ###
