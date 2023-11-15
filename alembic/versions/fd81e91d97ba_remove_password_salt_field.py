"""remove password salt field

Revision ID: fd81e91d97ba
Revises: 25d5eaf04a87
Create Date: 2023-11-15 08:09:23.350238

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'fd81e91d97ba'
down_revision: Union[str, None] = '25d5eaf04a87'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user_login', sa.Column('password', sa.String(length=250), nullable=True))
    op.drop_column('user_login', 'password_salt')
    op.drop_column('user_login', 'password_hash')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user_login', sa.Column('password_hash', sa.VARCHAR(length=250), autoincrement=False, nullable=True))
    op.add_column('user_login', sa.Column('password_salt', sa.VARCHAR(length=100), autoincrement=False, nullable=True))
    op.drop_column('user_login', 'password')
    # ### end Alembic commands ###