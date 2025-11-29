from app import create_app
import subprocess
import sys

app = create_app('development')

with app.app_context():
    result = subprocess.run(
        [sys.executable, '-m', 'flask', 'db', 'history'],
        capture_output=True,
        text=True,
        cwd=r'C:\Users\User\PycharmProjects\flask_app_Semkovych'
    )
    print(result.stdout)
    if result.stderr:
        print(result.stderr)