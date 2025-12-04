"""Insert data into products table

Revision ID: a6198b79831c
Revises: 28045c9a7dbc
Create Date: 2025-11-29 22:53:23.613883

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a6198b79831c'
down_revision = '28045c9a7dbc'
branch_labels = None
depends_on = None


def upgrade():
    categories_table = sa.table('categories',
                                sa.column('id', sa.Integer),
                                sa.column('name', sa.String)
                                )

    products_table = sa.table('products',
                              sa.column('name', sa.String),
                              sa.column('price', sa.Float),
                              sa.column('active', sa.Boolean),
                              sa.column('category_id', sa.Integer)
                              )

    op.bulk_insert(categories_table, [
        {'name': 'Electronics'},
        {'name': 'Books'},
        {'name': 'Clothing'},
    ])

    op.bulk_insert(products_table, [
        {'name': 'Laptop', 'price': 1200.0, 'active': True, 'category_id': 1},
        {'name': 'Smartphone', 'price': 800.0, 'active': True, 'category_id': 1},
        {'name': 'Novel', 'price': 20.0, 'active': True, 'category_id': 2},
        {'name': 'T-Shirt', 'price': 25.0, 'active': False, 'category_id': 3},
    ])


def downgrade():
    op.execute("""
        DELETE FROM products
        WHERE name IN ('Laptop', 'Smartphone', 'Novel', 'T-Shirt');
    """)

    op.execute("""
        DELETE FROM categories
        WHERE name IN ('Electronics', 'Books', 'Clothing');
    """)