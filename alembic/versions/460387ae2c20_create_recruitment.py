"""create recruitment

Revision ID: 460387ae2c20
Revises: 
Create Date: 2022-02-13 18:29:37.800556

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '460387ae2c20'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('recruitment'
            , sa.Column('recruitmentid', sa.Integer(),nullable=False, primary_key=True )
            , sa.Column('walletid', sa.Integer(),nullable=False)
            , sa.Column('walletaddress', sa.String(), nullable=False)
            , sa.Column('recruitingsamurais', sa.String(), nullable=True)
            , sa.Column('blockno', sa.Integer(), nullable=False)
            , sa.Column('missioncomplete', sa.Boolean(), nullable=False)
            , sa.Column('missionduration', sa.Integer(), nullable=False)         
    )
    pass


def downgrade():
    op.drop_table('recruitment')
    pass
