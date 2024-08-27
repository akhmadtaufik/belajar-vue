"""adding image_name, image_path, and created_at atribute on Tweets

Revision ID: f62b55373cf3
Revises: 51468cb447d2
Create Date: 2023-09-20 19:59:46.740267

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f62b55373cf3'
down_revision = '51468cb447d2'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('tweets', schema=None) as batch_op:
        batch_op.add_column(sa.Column('image_name', sa.String(length=128), nullable=True))
        batch_op.add_column(sa.Column('image_path', sa.String(length=1000), nullable=True))
        batch_op.add_column(sa.Column('created_at', sa.Integer(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('tweets', schema=None) as batch_op:
        batch_op.drop_column('created_at')
        batch_op.drop_column('image_path')
        batch_op.drop_column('image_name')

    # ### end Alembic commands ###
