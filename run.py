from app import create_app, db
from app.posts.models import Post
from app.products.models import Product, Category

app = create_app('development')


@app.shell_context_processor
def make_shell_context():
    return dict(db=db, Post=Post, Product=Product, Category=Category)


if __name__ == "__main__":
    app.run(debug=True)