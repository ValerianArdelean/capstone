"""empty message

Revision ID: 872e1d987cd2
Revises: 8df8bcbf6306
Create Date: 2020-10-15 21:24:11.720775

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '872e1d987cd2'
down_revision = '8df8bcbf6306'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('providers', sa.Column('services_offered', sa.String(length=200), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('providers', 'services_offered')
    # ### end Alembic commands ###
