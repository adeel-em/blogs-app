"""Initial migration

Revision ID: 187892efa1d0
Revises: 
Create Date: 2024-05-24 15:06:37.205724

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy import text



# revision identifiers, used by Alembic.
revision = '187892efa1d0'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():

    # create index for users table
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('first_name', sa.String(), nullable=False),
    sa.Column('last_name', sa.String(), nullable=False),
    sa.Column('username', sa.String(), nullable=False),
    sa.Column('email', sa.String(), nullable=False),
    sa.Column('password', sa.String(), nullable=False),
    sa.Column('role', sa.String(), nullable=False, default='user'),
    sa.Column('is_active', sa.Boolean(), nullable=False, default=True),
    sa.Column('created_at', sa.DateTime(), nullable=False, default=sa.func.now()),
    sa.Column('updated_at', sa.DateTime(), nullable=False, default=sa.func.now(), onupdate=sa.func.now()),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('username')
    )
    op.create_table('blogs',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(), nullable=False),
    sa.Column('content', sa.Text(), nullable=True),
    sa.Column('is_published', sa.Boolean(), nullable=False, default=True),
    sa.Column('created_at', sa.DateTime(), nullable=False, default=sa.func.now()),
    sa.Column('updated_at', sa.DateTime(), nullable=False, default=sa.func.now(), onupdate=sa.func.now()),
    sa.Column('owner_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['owner_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('comments',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('content', sa.Text(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False, default=sa.func.now()),
    sa.Column('updated_at', sa.DateTime(), nullable=False, default=sa.func.now(), onupdate=sa.func.now()),
    sa.Column('owner_id', sa.Integer(), nullable=False),
    sa.Column('blog_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['blog_id'], ['blogs.id'], ),
    sa.ForeignKeyConstraint(['owner_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )


def downgrade():

    # Drop the index first
    connection = op.get_bind()
    result = connection.execute(text("SELECT 1 FROM pg_indexes WHERE indexname = 'ix_blogs_title'"))
    if result.scalar():
        op.drop_index('ix_blogs_title', table_name='blogs')

    result = connection.execute(text("SELECT 1 FROM pg_indexes WHERE indexname = 'ix_comments_title'"))
    if result.scalar():
        op.drop_index('ix_comments_title', table_name='comments')

    result = connection.execute(text("SELECT 1 FROM pg_indexes WHERE indexname = 'ix_users_title'"))
    if result.scalar():
        op.drop_index('ix_users_title', table_name='users')

    op.drop_table('comments')
    op.drop_table('blogs')
    op.drop_table('users')