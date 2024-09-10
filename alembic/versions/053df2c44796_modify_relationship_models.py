"""Modify relationship models

Revision ID: 053df2c44796
Revises: a72bbe510ee1
Create Date: 2024-09-10 02:08:37.048345

"""
from typing import Sequence, Union
import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects.postgresql import UUID


# revision identifiers, used by Alembic.
revision: str = '053df2c44796'
down_revision: Union[str, None] = 'a72bbe510ee1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Check if the 'id' column exists before adding it
    conn = op.get_bind()
    inspector = sa.inspect(conn)
    columns = [col['name'] for col in inspector.get_columns('colors')]
    if 'id' not in columns:
        op.add_column('colors', sa.Column('id', UUID(as_uuid=True), primary_key=True, server_default=sa.text('uuid_generate_v4()')))

    # Drop the foreign key constraint
    op.drop_constraint('product_prices_color_id_fkey', 'product_prices', type_='foreignkey')

    # Recreate the foreign key constraint
    op.create_foreign_key(None, 'product_prices', 'colors', ['color_id'], ['id'])

    # Add other columns and perform other operations
    op.add_column('brands', sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False))
    op.add_column('brands', sa.Column('created_by', UUID(), nullable=True))
    op.add_column('brands', sa.Column('updated_at', sa.DateTime(), nullable=True))
    op.add_column('brands', sa.Column('updated_by', UUID(), nullable=True))
    op.add_column('brands', sa.Column('deleted_at', sa.DateTime(), nullable=True))
    op.drop_index('ix_brands_brand_id', table_name='brands')
    op.add_column('categories', sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False))
    op.add_column('categories', sa.Column('created_by', UUID(), nullable=True))
    op.add_column('categories', sa.Column('updated_at', sa.DateTime(), nullable=True))
    op.add_column('categories', sa.Column('updated_by', UUID(), nullable=True))
    op.add_column('categories', sa.Column('deleted_at', sa.DateTime(), nullable=True))
    op.drop_index('ix_categories_category_id', table_name='categories')
    op.add_column('colors', sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False))
    op.add_column('colors', sa.Column('created_by', UUID(), nullable=True))
    op.add_column('colors', sa.Column('updated_at', sa.DateTime(), nullable=True))
    op.add_column('colors', sa.Column('updated_by', UUID(), nullable=True))
    op.add_column('colors', sa.Column('deleted_at', sa.DateTime(), nullable=True))
    op.drop_index('ix_colors_color_id', table_name='colors')
    op.add_column('customers', sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False))
    op.add_column('customers', sa.Column('created_by', UUID(), nullable=True))
    op.add_column('customers', sa.Column('updated_at', sa.DateTime(), nullable=True))
    op.add_column('customers', sa.Column('updated_by', UUID(), nullable=True))
    op.add_column('customers', sa.Column('deleted_at', sa.DateTime(), nullable=True))
    op.add_column('locations', sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False))
    op.add_column('locations', sa.Column('created_by', UUID(), nullable=True))
    op.add_column('locations', sa.Column('updated_at', sa.DateTime(), nullable=True))
    op.add_column('locations', sa.Column('updated_by', UUID(), nullable=True))
    op.add_column('locations', sa.Column('deleted_at', sa.DateTime(), nullable=True))
    op.add_column('notifications', sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False))
    op.add_column('notifications', sa.Column('created_by', UUID(), nullable=True))
    op.add_column('notifications', sa.Column('updated_at', sa.DateTime(), nullable=True))
    op.add_column('notifications', sa.Column('updated_by', UUID(), nullable=True))
    op.add_column('notifications', sa.Column('deleted_at', sa.DateTime(), nullable=True))
    op.add_column('order_details', sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False))
    op.add_column('order_details', sa.Column('created_by', UUID(), nullable=True))
    op.add_column('order_details', sa.Column('updated_at', sa.DateTime(), nullable=True))
    op.add_column('order_details', sa.Column('updated_by', UUID(), nullable=True))
    op.add_column('order_details', sa.Column('deleted_at', sa.DateTime(), nullable=True))
    op.add_column('orders', sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False))
    op.add_column('orders', sa.Column('created_by', UUID(), nullable=True))
    op.add_column('orders', sa.Column('updated_at', sa.DateTime(), nullable=True))
    op.add_column('orders', sa.Column('updated_by', UUID(), nullable=True))
    op.add_column('orders', sa.Column('deleted_at', sa.DateTime(), nullable=True))
    op.add_column('payment_methods', sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False))
    op.add_column('payment_methods', sa.Column('created_by', UUID(), nullable=True))
    op.add_column('payment_methods', sa.Column('updated_at', sa.DateTime(), nullable=True))
    op.add_column('payment_methods', sa.Column('updated_by', UUID(), nullable=True))
    op.add_column('payment_methods', sa.Column('deleted_at', sa.DateTime(), nullable=True))
    op.add_column('product_prices', sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False))
    op.add_column('product_prices', sa.Column('created_by', UUID(), nullable=True))
    op.add_column('product_prices', sa.Column('updated_at', sa.DateTime(), nullable=True))
    op.add_column('product_prices', sa.Column('updated_by', UUID(), nullable=True))
    op.add_column('product_prices', sa.Column('deleted_at', sa.DateTime(), nullable=True))
    op.add_column('product_rates', sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False))
    op.add_column('product_rates', sa.Column('created_by', UUID(), nullable=True))
    op.add_column('product_rates', sa.Column('updated_at', sa.DateTime(), nullable=True))
    op.add_column('product_rates', sa.Column('updated_by', UUID(), nullable=True))
    op.add_column('product_rates', sa.Column('deleted_at', sa.DateTime(), nullable=True))
    op.add_column('products', sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False))
    op.add_column('products', sa.Column('created_by', UUID(), nullable=True))
    op.add_column('products', sa.Column('updated_at', sa.DateTime(), nullable=True))
    op.add_column('products', sa.Column('updated_by', UUID(), nullable=True))
    op.add_column('products', sa.Column('deleted_at', sa.DateTime(), nullable=True))
    op.add_column('staffs', sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False))
    op.add_column('staffs', sa.Column('created_by', UUID(), nullable=True))
    op.add_column('staffs', sa.Column('updated_at', sa.DateTime(), nullable=True))
    op.add_column('staffs', sa.Column('updated_by', UUID(), nullable=True))
    op.add_column('staffs', sa.Column('deleted_at', sa.DateTime(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # Drop the added columns
    op.drop_column('staffs', 'deleted_at')
    op.drop_column('staffs', 'updated_by')
    op.drop_column('staffs', 'updated_at')
    op.drop_column('staffs', 'created_by')
    op.drop_column('staffs', 'created_at')
    op.drop_column('products', 'deleted_at')
    op.drop_column('products', 'updated_by')
    op.drop_column('products', 'updated_at')
    op.drop_column('products', 'created_by')
    op.drop_column('products', 'created_at')
    op.drop_column('product_rates', 'deleted_at')
    op.drop_column('product_rates', 'updated_by')
    op.drop_column('product_rates', 'updated_at')
    op.drop_column('product_rates', 'created_by')
    op.drop_column('product_rates', 'created_at')
    op.drop_column('product_prices', 'deleted_at')
    op.drop_column('product_prices', 'updated_by')
    op.drop_column('product_prices', 'updated_at')
    op.drop_column('product_prices', 'created_by')
    op.drop_column('product_prices', 'created_at')
    op.drop_column('payment_methods', 'deleted_at')
    op.drop_column('payment_methods', 'updated_by')
    op.drop_column('payment_methods', 'updated_at')
    op.drop_column('payment_methods', 'created_by')
    op.drop_column('payment_methods', 'created_at')
    op.drop_column('orders', 'deleted_at')
    op.drop_column('orders', 'updated_by')
    op.drop_column('orders', 'updated_at')
    op.drop_column('orders', 'created_by')
    op.drop_column('orders', 'created_at')
    op.drop_column('order_details', 'deleted_at')
    op.drop_column('order_details', 'updated_by')
    op.drop_column('order_details', 'updated_at')
    op.drop_column('order_details', 'created_by')
    op.drop_column('order_details', 'created_at')
    op.drop_column('notifications', 'deleted_at')
    op.drop_column('notifications', 'updated_by')
    op.drop_column('notifications', 'updated_at')
    op.drop_column('notifications', 'created_by')
    op.drop_column('notifications', 'created_at')
    op.drop_column('locations', 'deleted_at')
    op.drop_column('locations', 'updated_by')
    op.drop_column('locations', 'updated_at')
    op.drop_column('locations', 'created_by')
    op.drop_column('locations', 'created_at')
    op.drop_column('customers', 'deleted_at')
    op.drop_column('customers', 'updated_by')
    op.drop_column('customers', 'updated_at')
    op.drop_column('customers', 'created_by')
    op.drop_column('customers', 'created_at')
    op.drop_column('colors', 'deleted_at')
    op.drop_column('colors', 'updated_by')
    op.drop_column('colors', 'updated_at')
    op.drop_column('colors', 'created_by')
    op.drop_column('colors', 'created_at')
    op.drop_column('categories', 'deleted_at')
    op.drop_column('categories', 'updated_by')
    op.drop_column('categories', 'updated_at')
    op.drop_column('categories', 'created_by')
    op.drop_column('categories', 'created_at')
    op.drop_column('brands', 'deleted_at')
    op.drop_column('brands', 'updated_by')
    op.drop_column('brands', 'updated_at')
    op.drop_column('brands', 'created_by')
    op.drop_column('brands', 'created_at')

    # Drop and recreate the foreign key constraint
    op.drop_constraint(None, 'product_prices', type_='foreignkey')
    op.create_foreign_key('product_prices_color_id_fkey', 'product_prices', 'colors', ['color_id'], ['id'])

    # Drop the 'id' column from 'colors' table
    op.drop_column('colors', 'id')
    # ### end Alembic commands ###
