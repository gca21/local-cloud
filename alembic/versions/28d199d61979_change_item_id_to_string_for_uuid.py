"""Change item id to string for uuid

Revision ID: 28d199d61979
Revises: 
Create Date: 2025-05-18 16:08:15.274544

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '28d199d61979'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('items',
    sa.Column('id', sa.String(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('is_dir', sa.Boolean(), nullable=False),
    sa.Column('parent_id', sa.String(), nullable=True),
    sa.Column('path', sa.String(), nullable=False),
    sa.Column('size', sa.Integer(), nullable=True),
    sa.Column('mimetype', sa.String(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['parent_id'], ['items.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('path')
    )
    op.create_index(op.f('ix_items_id'), 'items', ['id'], unique=False)
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(), nullable=False),
    sa.Column('password', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_id'), 'users', ['id'], unique=False)
    op.create_index(op.f('ix_users_username'), 'users', ['username'], unique=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_users_username'), table_name='users')
    op.drop_index(op.f('ix_users_id'), table_name='users')
    op.drop_table('users')
    op.drop_index(op.f('ix_items_id'), table_name='items')
    op.drop_table('items')
    # ### end Alembic commands ###
