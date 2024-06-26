"""empty message

Revision ID: b42b0cca15b2
Revises: e0770499d445
Create Date: 2024-06-07 10:33:50.187683

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b42b0cca15b2'
down_revision: Union[str, None] = 'e0770499d445'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('wallets',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('currency', sa.Enum('uds', 'eur', 'jpy', 'run', 'gbp', name='currencyenum'), nullable=False),
    sa.Column('amount', sa.Numeric(), nullable=False),
    sa.Column('owner_id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text("TIMEZONE('utc',now())"), nullable=False),
    sa.ForeignKeyConstraint(['owner_id'], ['users.id'], ondelete='SET NULL'),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('wallets')
    # ### end Alembic commands ###
