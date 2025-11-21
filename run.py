from app import create_app, db
from app.posts.models import Post

app = create_app('development')


@app.shell_context_processor
def make_shell_context():
    """Додає змінні в Flask shell"""
    return dict(db=db, Post=Post)


if __name__ == "__main__":
    app.run(debug=True)
