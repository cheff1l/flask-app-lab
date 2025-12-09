from app import create_app, db
from app.users.models import User

app = create_app('development')

with app.app_context():
    users = db.session.execute(db.select(User)).scalars().all()

    for user in users:
        if not user.image:
            user.image = 'profile_default.jpg'

    db.session.commit()
    print(f"✓ Оновлено {len(users)} користувачів!")
