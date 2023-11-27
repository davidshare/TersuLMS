"""update: text to question in QuizQuestion

Revision ID: a9cff2698dc0
Revises: bf42b5d817be
Create Date: 2023-11-27 08:34:30.790798

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a9cff2698dc0'
down_revision: Union[str, None] = 'bf42b5d817be'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('quiz_questions', sa.Column('question', sa.Text(), nullable=False))
    op.drop_column('quiz_questions', 'text')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('quiz_questions', sa.Column('text', sa.TEXT(), autoincrement=False, nullable=False))
    op.drop_column('quiz_questions', 'question')
    # ### end Alembic commands ###
