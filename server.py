import os
import socket
import subprocess

from flask import Flask, render_template, request

app = Flask(__name__)

DEBUG = True if os.environ.get('DEBUG') else False

def debug(msg):
    if DEBUG:
        print('debug:', msg)

def applescript(cmd):
    result = subprocess.run(['osascript', '-e', cmd], capture_output=True, text=True)
    return result.stdout

def get_volume():
    debug('get_volume()')
    value = applescript('output volume of (get volume settings)')
    return int(value)

def set_volume(volume):
    debug('set_volume(): volume={}'.format(volume))
    applescript('set volume output volume {0}'.format(volume))

def get_mute():
    debug('get_mute()')
    value = applescript('output muted of (get volume settings)')
    return value.strip() == 'true'

def set_mute(mute):
    debug('set_mute(): mute={}'.format(mute))
    applescript('set volume output muted {0}'.format('true' if mute else 'false'))

@app.route('/volume', methods=['GET', 'POST'])
def handle_volume():
    if request.method == 'POST':
        value = request.json['volume']
        set_volume(value)
        return {'volume': value}
    else:
        return {'volume': get_volume()}

@app.route('/mute', methods=['GET', 'POST'])
def handle_mute():
    if request.method == 'POST':
        value = request.json['mute']
        set_mute(value)
        return {'mute': value}
    else:
        return {'mute': get_mute()}

@app.route('/')
def handle_index():
    return render_template('index.html', hostname=socket.gethostname())

def main():
    set_volume(33)

if __name__ == '__main__':
    main()

