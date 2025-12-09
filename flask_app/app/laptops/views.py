from flask import render_template, request, redirect, url_for, flash, abort
from flask_login import login_required, current_user
from . import laptops_bp
from .forms import LaptopForm, SearchForm
from .models import Laptop, LaptopCategory
from app import db


@laptops_bp.route('/')
def index():
    search_form = SearchForm()
    search_query = request.args.get('search_query', '')

    query = db.select(Laptop).order_by(Laptop.created_at.desc())

    if search_query:
        query = query.where(
            (Laptop.brand.ilike(f'%{search_query}%')) |
            (Laptop.model.ilike(f'%{search_query}%'))
        )

    laptops = db.session.execute(query).scalars().all()

    return render_template('laptops/index.html',
                           laptops=laptops,
                           search_form=search_form,
                           search_query=search_query)


@laptops_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    form = LaptopForm()

    categories = db.session.execute(db.select(LaptopCategory)).scalars().all()
    form.category_id.choices = [(c.id, c.category_name) for c in categories]

    if form.validate_on_submit():
        laptop = Laptop(
            brand=form.brand.data,
            model=form.model.data,
            price=form.price.data,
            description=form.description.data,
            category_id=form.category_id.data,
            user_id=current_user.id
        )
        db.session.add(laptop)
        db.session.commit()
        flash('Laptop created successfully!', 'success')
        return redirect(url_for('laptops.index'))

    return render_template('laptops/create.html', form=form)


@laptops_bp.route('/<int:laptop_id>')
def detail(laptop_id):
    laptop = db.session.get(Laptop, laptop_id)
    if not laptop:
        abort(404)
    return render_template('laptops/detail.html', laptop=laptop)


@laptops_bp.route('/<int:laptop_id>/edit', methods=['GET', 'POST'])
@login_required
def edit(laptop_id):
    laptop = db.session.get(Laptop, laptop_id)
    if not laptop:
        abort(404)

    if laptop.user_id != current_user.id:
        flash('You can only edit your own laptops!', 'danger')
        return redirect(url_for('laptops.detail', laptop_id=laptop_id))

    form = LaptopForm()

    categories = db.session.execute(db.select(LaptopCategory)).scalars().all()
    form.category_id.choices = [(c.id, c.category_name) for c in categories]

    if form.validate_on_submit():
        laptop.brand = form.brand.data
        laptop.model = form.model.data
        laptop.price = form.price.data
        laptop.description = form.description.data
        laptop.category_id = form.category_id.data
        db.session.commit()
        flash('Laptop updated successfully!', 'success')
        return redirect(url_for('laptops.detail', laptop_id=laptop_id))

    elif request.method == 'GET':
        form.brand.data = laptop.brand
        form.model.data = laptop.model
        form.price.data = laptop.price
        form.description.data = laptop.description
        form.category_id.data = laptop.category_id

    return render_template('laptops/edit.html', form=form, laptop=laptop)


@laptops_bp.route('/<int:laptop_id>/delete', methods=['POST'])
@login_required
def delete(laptop_id):
    laptop = db.session.get(Laptop, laptop_id)
    if not laptop:
        abort(404)

    if laptop.user_id != current_user.id:
        flash('You can only delete your own laptops!', 'danger')
        return redirect(url_for('laptops.detail', laptop_id=laptop_id))

    db.session.delete(laptop)
    db.session.commit()
    flash('Laptop deleted successfully!', 'success')
    return redirect(url_for('laptops.index'))