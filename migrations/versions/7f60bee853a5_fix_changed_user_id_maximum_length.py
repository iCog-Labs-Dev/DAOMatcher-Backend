"""fix: Changed user id maximum length

Revision ID: 7f60bee853a5
Revises: f6d21ab19f48
Create Date: 2024-05-10 18:04:37.594424

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7f60bee853a5'
down_revision = 'f6d21ab19f48'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.alter_column('id',
               existing_type=sa.VARCHAR(length=60),
               type_=sa.String(length=50),
               existing_nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.alter_column('id',
               existing_type=sa.String(length=50),
               type_=sa.VARCHAR(length=60),
               existing_nullable=False)

    # ### end Alembic commands ###
