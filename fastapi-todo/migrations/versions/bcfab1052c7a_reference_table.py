"""reference_table

Revision ID: bcfab1052c7a
Revises: d66b22b47bb2
Create Date: 2024-09-24 16:59:12.927219

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'bcfab1052c7a'
down_revision: Union[str, None] = 'd66b22b47bb2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('reference_token', sa.String(length=512), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'reference_token')
    # ### end Alembic commands ###
