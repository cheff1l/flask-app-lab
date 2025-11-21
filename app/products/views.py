from flask import render_template, request
from . import products_bp


@products_bp.route('/')
def index():
    return render_template("products/index.html", title="Продукти")


@products_bp.route('/<int:product_id>')
def product_detail(product_id):
    product = {
        'id': product_id,
        'name': f'Продукт {product_id}',
        'price': product_id * 10.5,
        'description': f'Опис продукту {product_id}'
    }

    return render_template("products/detail.html",
                           title=f"Продукт {product_id}",
                           product=product)