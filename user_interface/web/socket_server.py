from flask import Flask
from flask_socketio import SocketIO

async_mode = 'gevent'
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app,
                    async_mode=async_mode,
                    # manage_session=True,
                    cookie='cookie',
                    name="server",
                    logger=True)
