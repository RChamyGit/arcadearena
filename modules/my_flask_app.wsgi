activate_this = '/arcadearena/venv/bin/my_app.py'
with open(activate_this) as file_:
    exec(file_.read(), dict(__file__=activate_this))

import logging
import sys
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0, '/home/arcade/ArenaApp/')
from my_flask_app import app as application
application.secret_key = 'TEstes'
