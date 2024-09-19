"""add media_storage_v3

Revision ID: 435d7bfa1f19
Revises: 37afd7ba055e
Create Date: 2024-09-19 14:24:25.824788

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '435d7bfa1f19'
down_revision: Union[str, None] = '37afd7ba055e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('media_storages',
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('unique_name', sa.String(), nullable=True),
    sa.Column('extension', sa.String(), nullable=True),
    sa.Column('uri', sa.String(), nullable=True),
    sa.Column('created_on', sa.DateTime(), nullable=True),
    sa.Column('reference_id', sa.UUID(), nullable=True),
    sa.Column('entity_type', sa.String(), nullable=True),
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('created_by', sa.UUID(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('updated_by', sa.UUID(), nullable=True),
    sa.Column('deleted_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('media_storages')
    # ### end Alembic commands ###
