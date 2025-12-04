from flask import render_template, request, redirect, url_for, flash, session
from app import db
from app.posts import posts_bp
from app.posts.models import Post, Tag
from app.posts.forms import PostForm
from app.users.models import User


@posts_bp.route('/create', methods=['GET', 'POST'])
def add_post():
    form = PostForm()
    
    authors = db.session.execute(db.select(User)).scalars().all()
    form.author_id.choices = [(author.id, author.username) for author in authors]
    
    tags = db.session.execute(db.select(Tag)).scalars().all()
    form.tags.choices = [(tag.id, tag.name) for tag in tags]
    
    if form.validate_on_submit():
        new_post = Post(
            title=form.title.data,
            content=form.content.data,
            is_active=form.is_active.data,
            posted=form.publish_date.data,
            category=form.category.data,
            user_id=form.author_id.data
        )
        
        selected_tags = db.session.execute(
            db.select(Tag).where(Tag.id.in_(form.tags.data))
        ).scalars().all()
        new_post.tags = selected_tags
        
        db.session.add(new_post)
        db.session.commit()
        
        flash(f"Post '{form.title.data}' has been added.", 'success')
        return redirect(url_for('posts.all_posts'))
    
    elif request.method == "POST":
        flash("Enter the correct data in the form!", "danger")
    
    return render_template('add_post.html', form=form)


@posts_bp.route('')
@posts_bp.route('/')
def all_posts():
    stmt = db.select(Post).where(Post.is_active == True).order_by(Post.posted.desc())
    posts = db.session.scalars(stmt).all()
    
    return render_template('posts.html', posts=posts)


@posts_bp.route('/<int:id>')
def detail_post(id):
    post = db.get_or_404(Post, id)
    return render_template('detail_post.html', post=post)


@posts_bp.route('/<int:id>/update', methods=['GET', 'POST'])
def edit_post(id):
    post = db.get_or_404(Post, id)
    form = PostForm(obj=post)

    form.publish_date.data = post.posted
    
    authors = db.session.execute(db.select(User)).scalars().all()
    form.author_id.choices = [(author.id, author.username) for author in authors]
    
    tags = db.session.execute(db.select(Tag)).scalars().all()
    form.tags.choices = [(tag.id, tag.name) for tag in tags]
    
    if request.method == 'GET':
        form.author_id.data = post.user_id
        form.tags.data = [tag.id for tag in post.tags]
    
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        post.is_active = form.is_active.data
        post.posted = form.publish_date.data
        post.category = form.category.data
        post.user_id = form.author_id.data
        
        selected_tags = db.session.execute(
            db.select(Tag).where(Tag.id.in_(form.tags.data))
        ).scalars().all()
        post.tags = selected_tags
        
        db.session.commit()
        flash("Post updated!", "success")
        return redirect(url_for('posts.detail_post', id=post.id))
    
    return render_template('add_post.html', form=form, title='Edit Post')


@posts_bp.route('/<int:id>/delete', methods=['GET', 'POST'])
def delete_post(id):
    post = db.get_or_404(Post, id)
    
    if request.method == 'POST':
        db.session.delete(post)
        db.session.commit()
        flash("Post successfully deleted.", "danger")
        return redirect(url_for('posts.all_posts'))
    
    return render_template('delete_confirm.html', post=post)
