from flask import Flask
from flask_socketio import SocketIO

from settings import DIR_ROOT

async_mode = 'gevent'
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
app.config['UPLOAD_FOLDER'] = DIR_ROOT + 'storage/english_words/'
socketio = SocketIO(app,
                    # async_mode=async_mode,
                    # manage_session=True,
                    cookie='cookie',
                    name="server",
                    logger=True)
