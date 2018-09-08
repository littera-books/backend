import os
import json

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SECRET_FILE = os.path.join(ROOT_DIR, '.secrets.json')

with open(SECRET_FILE, 'r') as secrets:
    secret_data = secrets.read()

secret_json = json.loads(secret_data)
