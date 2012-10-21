import sys, os

# Switch to the virtualenv if we're not already there
INTERP = os.path.expanduser("~/env/chatterbox/bin/python")
if sys.executable != INTERP: os.execl(INTERP, INTERP, *sys.argv)

__import__('Chatterbox/wsgi-test-socketio.py')
