"""fix: Foreign key interdependecy

Revision ID: 439ae76427a9
Revises: 5b0b7205085d
Create Date: 2024-03-29 09:44:24.547766

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '439ae76427a9'
down_revision = '5b0b7205085d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user_setting', schema=None) as batch_op:
        batch_op.drop_constraint('user_setting_ibfk_1', type_='foreignkey')
        batch_op.drop_column('user_id')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user_setting', schema=None) as batch_op:
        batch_op.add_column(sa.Column('user_id', mysql.VARCHAR(length=50), nullable=False))
        batch_op.create_foreign_key('user_setting_ibfk_1', 'user', ['user_id'], ['id'])

    # ### end Alembic commands ###