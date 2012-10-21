import cgi
import os.path
import mimetypes

from socketio import socketio_manage
from socketio.server import SocketIOServer
from socketio.namespace import BaseNamespace

def main():
    server = SocketIOServer(
        ('', 8080), application,
        policy_server=False)
    server.serve_forever()

def application(environ, start_response):
    if environ["PATH_INFO"].startswith('/socket.io/'):
        return socketio_manage(environ, { '/chat': ChatNamespace })
    else:
        return serve_file(environ, start_response)

def serve_file(environ, start_response):
    path = environ['PATH_INFO'].lstrip('/')
    if not path:
        path = 'index.html'
    if os.path.exists(path):
        ctype = mimetypes.guess_type(path)
        if ctype is None: ctype='application/octet-stream'
        else: ctype = ctype[0]
        start_response('200 OK', [('Content-Type', ctype)])
        for line in open(path):
            yield line
    else:
        start_response('404 NOT FOUND', [])
        yield 'File not found'

class ChatNamespace(BaseNamespace):
    connections = {}

    def initialize(self):
        self.key = '0x%x' % id(self)
        self.connections[self.key] = self
        self.nick = self.key

    def disconnect(self, *args, **kwargs):
        del self.connections[self.key]
        super(ChatNamespace, self).disconnect(*args, **kwargs)

    def on_chat(self, message):
        if message.startswith('/nick '):
            self.nick = message.split(' ', 1)[-1]
            return
        message = '%s: %s' % (self.nick, message)
        for ns in self.connections.values():
            ns.emit('chat', cgi.escape(message))


if __name__ == '__main__':
    main()
