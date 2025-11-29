from flask import render_template
from app.products import products_bp
from app.products.models import Product
from app import db
from sqlalchemy import select


@products_bp.route('/')
def index():
    stmt = select(Product).order_by(Product.id)
    products = db.session.execute(stmt).scalars().all()
    return render_template('products/index.html', products=products, title="Продукти")


@products_bp.route('/<int:product_id>')
def product_detail(product_id):
    product = db.get_or_404(Product, product_id)
    return render_template('products/detail.html', product=product, title=product.name)