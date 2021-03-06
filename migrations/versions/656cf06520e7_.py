"""empty message

Revision ID: 656cf06520e7
Revises: fe2e89a2eda2
Create Date: 2019-01-21 16:34:44.309510

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '656cf06520e7'
down_revision = 'fe2e89a2eda2'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('validation_error', sa.Column('url', sa.String(length=200), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('validation_error', 'url')
    # ### end Alembic commands ###
