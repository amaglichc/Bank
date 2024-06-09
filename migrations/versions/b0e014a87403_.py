"""empty message

Revision ID: b0e014a87403
Revises: d569e627b99e
Create Date: 2024-06-09 10:56:03.155259

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b0e014a87403'
down_revision: Union[str, None] = 'd569e627b99e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('transfers', sa.Column('to_wallet_id', sa.Integer(), nullable=False))
    op.create_foreign_key(None, 'transfers', 'wallets', ['to_wallet_id'], ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'transfers', type_='foreignkey')
    op.drop_column('transfers', 'to_wallet_id')
    # ### end Alembic commands ###