"""create table recruitment

Revision ID: 0b6e173ff810
Revises: 
Create Date: 2022-02-11 00:23:59.200738

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.engine import reflection


# revision identifiers, used by Alembic.
revision = '0b6e173ff810'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('recruitment'
                , sa.Column('recruitmentid', sa.Integer(),nullable=False, primary_key=True )
                , sa.Column('walletid', sa.Integer(),nullable=False)
                , sa.Column('walletaddress', sa.String(), nullable=False)
                , sa.Column('recruitingssamurais', sa.String(), nullable=True)
                , sa.Column('blockno', sa.Integer(), nullable=False)
                , sa.Column('missioncomplete', sa.Boolean(), nullable=False)
    )
    pass


def downgrade():
    op.drop_table('recruitment')
    pass



