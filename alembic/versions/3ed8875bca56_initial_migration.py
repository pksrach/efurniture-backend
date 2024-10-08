"""Initial migration

Revision ID: 3ed8875bca56
Revises: 
Create Date: 2024-09-06 19:08:38.617325

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3ed8875bca56'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('brands',
    sa.Column('brand_id', sa.UUID(), nullable=False),
    sa.Column('code', sa.String(length=100), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('attachment', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('brand_id')
    )
    op.create_index(op.f('ix_brands_brand_id'), 'brands', ['brand_id'], unique=False)
    op.create_table('categories',
    sa.Column('category_id', sa.UUID(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('attachment', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('category_id')
    )
    op.create_index(op.f('ix_categories_category_id'), 'categories', ['category_id'], unique=False)
    op.create_table('colors',
    sa.Column('color_id', sa.UUID(), nullable=False),
    sa.Column('code', sa.String(length=100), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('highlight', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('color_id')
    )
    op.create_index(op.f('ix_colors_color_id'), 'colors', ['color_id'], unique=False)
    op.create_table('locations',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('price', sa.Float(), nullable=True),
    sa.Column('parent_id', sa.UUID(), nullable=True),
    sa.ForeignKeyConstraint(['parent_id'], ['locations.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('payment_methods',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('attachment_qr', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('users',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('name', sa.String(length=150), nullable=True),
    sa.Column('email', sa.String(length=255), nullable=True),
    sa.Column('mobile', sa.String(length=20), nullable=True),
    sa.Column('password', sa.String(length=100), nullable=True),
    sa.Column('is_active', sa.Boolean(), nullable=True),
    sa.Column('verified_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)
    op.create_index(op.f('ix_users_mobile'), 'users', ['mobile'], unique=False)
    op.create_table('customers',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('gender', sa.Integer(), nullable=True),
    sa.Column('address', sa.String(), nullable=True),
    sa.Column('phone_number', sa.String(), nullable=True),
    sa.Column('user_id', sa.UUID(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('notifications',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('from_user_id', sa.UUID(), nullable=True),
    sa.Column('to_user_id', sa.UUID(), nullable=True),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('date', sa.Date(), nullable=True),
    sa.Column('type', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['from_user_id'], ['users.id'], ),
    sa.ForeignKeyConstraint(['to_user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('products',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('attachment', sa.String(), nullable=True),
    sa.Column('is_active', sa.Boolean(), nullable=True),
    sa.Column('category_id', sa.UUID(), nullable=True),
    sa.Column('brand_id', sa.UUID(), nullable=True),
    sa.ForeignKeyConstraint(['brand_id'], ['brands.brand_id'], ),
    sa.ForeignKeyConstraint(['category_id'], ['categories.category_id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('staffs',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('gender', sa.Integer(), nullable=True),
    sa.Column('address', sa.String(), nullable=True),
    sa.Column('phone_number', sa.String(), nullable=True),
    sa.Column('salary', sa.Float(), nullable=True),
    sa.Column('user_id', sa.UUID(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user_tokens',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('user_id', sa.UUID(), nullable=False),
    sa.Column('access_key', sa.String(length=250), nullable=True),
    sa.Column('refresh_key', sa.String(length=250), nullable=True),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('expires_at', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_tokens_access_key'), 'user_tokens', ['access_key'], unique=False)
    op.create_index(op.f('ix_user_tokens_refresh_key'), 'user_tokens', ['refresh_key'], unique=False)
    op.create_table('orders',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('order_date', sa.Date(), nullable=False),
    sa.Column('customer_id', sa.UUID(), nullable=True),
    sa.Column('location_id', sa.UUID(), nullable=True),
    sa.Column('location_price', sa.Float(), nullable=True),
    sa.Column('total', sa.Float(), nullable=True),
    sa.Column('discount', sa.Float(), nullable=True),
    sa.Column('amount', sa.Float(), nullable=True),
    sa.Column('payment_method_id', sa.UUID(), nullable=True),
    sa.Column('payment_attachment', sa.String(), nullable=True),
    sa.Column('order_status', sa.String(), nullable=True),
    sa.Column('note', sa.String(), nullable=True),
    sa.Column('staff_id', sa.UUID(), nullable=True),
    sa.ForeignKeyConstraint(['customer_id'], ['customers.id'], ),
    sa.ForeignKeyConstraint(['location_id'], ['locations.id'], ),
    sa.ForeignKeyConstraint(['payment_method_id'], ['payment_methods.id'], ),
    sa.ForeignKeyConstraint(['staff_id'], ['staffs.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('product_prices',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('price', sa.Float(), nullable=True),
    sa.Column('color_id', sa.UUID(), nullable=True),
    sa.Column('size', sa.String(), nullable=True),
    sa.Column('product_id', sa.UUID(), nullable=True),
    sa.ForeignKeyConstraint(['color_id'], ['colors.color_id'], ),
    sa.ForeignKeyConstraint(['product_id'], ['products.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('product_rates',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('user_id', sa.UUID(), nullable=True),
    sa.Column('product_id', sa.UUID(), nullable=True),
    sa.Column('rate', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['product_id'], ['products.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('order_details',
    sa.Column('id', sa.UUID(), nullable=False),
    sa.Column('order_id', sa.UUID(), nullable=True),
    sa.Column('product_price_id', sa.UUID(), nullable=True),
    sa.Column('price', sa.Float(), nullable=True),
    sa.Column('qty', sa.Integer(), nullable=True),
    sa.Column('total', sa.Float(), nullable=True),
    sa.Column('discount', sa.Float(), nullable=True),
    sa.Column('amount', sa.Float(), nullable=True),
    sa.ForeignKeyConstraint(['order_id'], ['orders.id'], ),
    sa.ForeignKeyConstraint(['product_price_id'], ['product_prices.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('order_details')
    op.drop_table('product_rates')
    op.drop_table('product_prices')
    op.drop_table('orders')
    op.drop_index(op.f('ix_user_tokens_refresh_key'), table_name='user_tokens')
    op.drop_index(op.f('ix_user_tokens_access_key'), table_name='user_tokens')
    op.drop_table('user_tokens')
    op.drop_table('staffs')
    op.drop_table('products')
    op.drop_table('notifications')
    op.drop_table('customers')
    op.drop_index(op.f('ix_users_mobile'), table_name='users')
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_table('users')
    op.drop_table('payment_methods')
    op.drop_table('locations')
    op.drop_index(op.f('ix_colors_color_id'), table_name='colors')
    op.drop_table('colors')
    op.drop_index(op.f('ix_categories_category_id'), table_name='categories')
    op.drop_table('categories')
    op.drop_index(op.f('ix_brands_brand_id'), table_name='brands')
    op.drop_table('brands')
    # ### end Alembic commands ###
