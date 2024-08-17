"""empty message

Revision ID: 70c11d52719a
Revises: 48973ae9bef1
Create Date: 2024-08-17 17:33:30.966549

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '70c11d52719a'
down_revision = '48973ae9bef1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user_result',
    sa.Column('id', sa.String(length=50), nullable=False),
    sa.Column('username', sa.String(length=256), nullable=False),
    sa.Column('type', sa.String(length=20), nullable=False),
    sa.Column('score', sa.Integer(), nullable=True),
    sa.Column('handle', sa.String(length=256), nullable=True),
    sa.Column('social_media', sa.String(length=256), nullable=True),
    sa.Column('image_url', sa.String(length=256), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user_setting',
    sa.Column('id', sa.String(length=50), nullable=False),
    sa.Column('default_user_count', sa.Integer(), nullable=False),
    sa.Column('default_depth_count', sa.Integer(), nullable=False),
    sa.Column('theme', sa.String(length=10), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user_usage',
    sa.Column('id', sa.String(length=50), nullable=False),
    sa.Column('token_count', sa.Integer(), nullable=False),
    sa.Column('search_count', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user',
    sa.Column('id', sa.String(length=50), nullable=False),
    sa.Column('email', sa.String(length=100), nullable=False),
    sa.Column('verified', sa.Boolean(), nullable=False),
    sa.Column('display_name', sa.String(length=50), nullable=False),
    sa.Column('password', sa.String(length=200), nullable=True),
    sa.Column('password_salt', sa.String(length=200), nullable=True),
    sa.Column('api_key', sa.String(length=50), nullable=True),
    sa.Column('user_setting_id', sa.String(length=50), nullable=True),
    sa.Column('usage_id', sa.String(length=50), nullable=True),
    sa.ForeignKeyConstraint(['usage_id'], ['user_usage.id'], ),
    sa.ForeignKeyConstraint(['user_setting_id'], ['user_setting.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    op.create_table('search_result',
    sa.Column('id', sa.String(length=50), nullable=False),
    sa.Column('time_stamp', sa.DateTime(), nullable=False),
    sa.Column('description', sa.String(length=250), nullable=False),
    sa.Column('user_id', sa.String(length=50), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('search_user_results',
    sa.Column('search_id', sa.String(length=50), nullable=False),
    sa.Column('user_result_id', sa.String(length=50), nullable=False),
    sa.Column('type', sa.Enum('SEED', 'FOUND', name='usernametype'), nullable=True),
    sa.ForeignKeyConstraint(['search_id'], ['search_result.id'], ),
    sa.ForeignKeyConstraint(['user_result_id'], ['user_result.id'], ),
    sa.PrimaryKeyConstraint('search_id', 'user_result_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('search_user_results')
    op.drop_table('search_result')
    op.drop_table('user')
    op.drop_table('user_usage')
    op.drop_table('user_setting')
    op.drop_table('user_result')
    # ### end Alembic commands ###
