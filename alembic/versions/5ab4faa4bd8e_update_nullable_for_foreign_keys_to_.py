"""update nullable for foreign keys to false

Revision ID: 5ab4faa4bd8e
Revises: 01b006a55789
Create Date: 2023-12-03 17:36:14.822817

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5ab4faa4bd8e'
down_revision: Union[str, None] = '01b006a55789'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('article_content', 'lesson_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.alter_column('file_content', 'lesson_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.alter_column('lessons', 'course_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.alter_column('lessons', 'section_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.alter_column('quiz_content', 'lesson_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('quiz_content', 'lesson_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.alter_column('lessons', 'section_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.alter_column('lessons', 'course_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.alter_column('file_content', 'lesson_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.alter_column('article_content', 'lesson_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    # ### end Alembic commands ###
