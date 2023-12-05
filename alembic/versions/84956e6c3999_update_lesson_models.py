"""update: lesson models

Revision ID: 84956e6c3999
Revises: e1538b8bdc36
Create Date: 2023-12-03 03:25:48.776698

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '84956e6c3999'
down_revision: Union[str, None] = 'e1538b8bdc36'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('file_content',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('lesson_id', sa.Integer(), nullable=True),
    sa.Column('url', sa.String(length=255), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['lesson_id'], ['lessons.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('video_content')
    op.drop_table('quiz_option')
    op.drop_table('quiz_questions')
    op.add_column('article_content', sa.Column('content', sa.Text(), nullable=False))
    op.drop_constraint('article_content_text_key', 'article_content', type_='unique')
    op.drop_column('article_content', 'text')
    op.add_column('lessons', sa.Column('quiz_attempts_allowed', sa.Integer(), nullable=False))
    op.add_column('quiz_content', sa.Column('question', sa.Text(), nullable=False))
    op.add_column('quiz_content', sa.Column('option_1', sa.Text(), nullable=False))
    op.add_column('quiz_content', sa.Column('option_2', sa.Text(), nullable=False))
    op.add_column('quiz_content', sa.Column('option_3', sa.Text(), nullable=True))
    op.add_column('quiz_content', sa.Column('option_4', sa.Text(), nullable=True))
    op.add_column('quiz_content', sa.Column('answer', sa.Text(), nullable=False))
    op.drop_column('quiz_content', 'attempts_allowed')
    op.drop_column('quiz_content', 'published')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('quiz_content', sa.Column('published', sa.BOOLEAN(), autoincrement=False, nullable=True))
    op.add_column('quiz_content', sa.Column('attempts_allowed', sa.INTEGER(), autoincrement=False, nullable=False))
    op.drop_column('quiz_content', 'answer')
    op.drop_column('quiz_content', 'option_4')
    op.drop_column('quiz_content', 'option_3')
    op.drop_column('quiz_content', 'option_2')
    op.drop_column('quiz_content', 'option_1')
    op.drop_column('quiz_content', 'question')
    op.drop_column('lessons', 'quiz_attempts_allowed')
    op.add_column('article_content', sa.Column('text', sa.TEXT(), autoincrement=False, nullable=False))
    op.create_unique_constraint('article_content_text_key', 'article_content', ['text'])
    op.drop_column('article_content', 'content')
    op.create_table('quiz_questions',
    sa.Column('id', sa.INTEGER(), server_default=sa.text("nextval('quiz_questions_id_seq'::regclass)"), autoincrement=True, nullable=False),
    sa.Column('quiz_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('question', sa.TEXT(), autoincrement=False, nullable=False),
    sa.Column('lesson_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['lesson_id'], ['lessons.id'], name='quiz_questions_lesson_id_fkey'),
    sa.ForeignKeyConstraint(['quiz_id'], ['quiz_content.id'], name='quiz_questions_quiz_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='quiz_questions_pkey'),
    sa.UniqueConstraint('lesson_id', 'question', name='_lesson_question_uc'),
    postgresql_ignore_search_path=False
    )
    op.create_table('quiz_option',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('question_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('text', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('is_correct', sa.BOOLEAN(), autoincrement=False, nullable=True),
    sa.Column('created_at', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.Column('updated_at', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['question_id'], ['quiz_questions.id'], name='quiz_option_question_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='quiz_option_pkey'),
    sa.UniqueConstraint('question_id', 'text', name='_question_option_text_uc')
    )
    op.create_table('video_content',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('lesson_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('url', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('description', sa.TEXT(), autoincrement=False, nullable=False),
    sa.Column('duration', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('created_at', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.Column('updated_at', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['lesson_id'], ['lessons.id'], name='video_content_lesson_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='video_content_pkey'),
    sa.UniqueConstraint('url', name='video_content_url_key')
    )
    op.drop_table('file_content')
    # ### end Alembic commands ###