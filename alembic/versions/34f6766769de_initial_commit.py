"""Initial Commit

Revision ID: 34f6766769de
Revises: 
Create Date: 2024-07-09 15:14:18.336274

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '34f6766769de'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('userId', sa.String(length=50), nullable=False),
    sa.Column('firstName', sa.String(length=50), nullable=False),
    sa.Column('lastName', sa.String(length=50), nullable=False),
    sa.Column('email', sa.String(length=120), nullable=False),
    sa.Column('password', sa.String(length=350), nullable=False),
    sa.Column('phone', sa.String(length=20), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('userId')
    )
    op.create_table('organisation',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('orgId', sa.String(length=50), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('description', sa.String(length=200), nullable=True),
    sa.Column('creator_id', sa.String(length=36), nullable=False),
    sa.ForeignKeyConstraint(['creator_id'], ['user.userId']),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('orgId')
    )
    op.create_table('organisation_user',
    sa.Column('userId', sa.String(length=36), nullable=False),
    sa.Column('orgId', sa.String(length=36), nullable=False),
    sa.ForeignKeyConstraint(['orgId'], ['organisation.orgId'], ),
    sa.ForeignKeyConstraint(['userId'], ['user.userId'], ),
    sa.PrimaryKeyConstraint('userId', 'orgId')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    pass
    # ### end Alembic commands ###