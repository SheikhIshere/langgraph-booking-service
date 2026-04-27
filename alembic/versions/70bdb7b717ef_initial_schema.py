"""Initial schema

Revision ID: 70bdb7b717ef
Revises: 
Create Date: 2026-04-27 15:27:02.901893

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '70bdb7b717ef'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('conversations',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('conversation_id', sa.String(length=255), nullable=False),
    sa.Column('role', sa.String(length=50), nullable=False),
    sa.Column('content', sa.Text(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_conversations_conversation_id'), 'conversations', ['conversation_id'], unique=False)
    op.create_table('listings',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('title', sa.String(length=255), nullable=False),
    sa.Column('location', sa.String(length=255), nullable=False),
    sa.Column('price_per_night_bdt', sa.Numeric(precision=10, scale=2), nullable=False),
    sa.Column('max_guests', sa.Integer(), nullable=False),
    sa.Column('is_available', sa.Boolean(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('bookings',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('listing_id', sa.UUID(), nullable=False),
    sa.Column('guest_name', sa.String(length=255), nullable=False),
    sa.Column('check_in', sa.Date(), nullable=False),
    sa.Column('check_out', sa.Date(), nullable=False),
    sa.Column('total_price', sa.Numeric(precision=10, scale=2), nullable=False),
    sa.Column('status', sa.String(length=50), nullable=False),
    sa.ForeignKeyConstraint(['listing_id'], ['listings.id'], ),
    sa.PrimaryKeyConstraint('id')
    )


def downgrade() -> None:
    op.drop_table('bookings')
    op.drop_table('listings')
    op.drop_index(op.f('ix_conversations_conversation_id'), table_name='conversations')
    op.drop_table('conversations')
