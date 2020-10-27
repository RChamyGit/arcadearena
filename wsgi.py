from gevent.pywsgi import WSGIServer
from my_flask_app import app

http_server = WSGIServer((), app)
http_server.serve_forever()