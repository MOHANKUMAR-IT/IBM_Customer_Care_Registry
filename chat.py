from flask import Flask, render_template
from flask_socketio import SocketIO
from flask_socketio import send, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)
# socketio = SocketIO(app,logger=True, engineio_logger=True)
@app.route("/")
def chat_app():
    return render_template("chat.html")

#receive
@socketio.on('message')
def handle_message(data):
    print('received message: ' + data)
    
@socketio.on('json')
def handle_json(json):
    print('received json: ' + str(json))

@socketio.on("my event")
def handle_message(data):
    print(data)

@socketio.on('my event')
def handle_my_custom_event(json):
    print('received json: ' + str(json))

#sending
@socketio.on('message')
def handle_message(message):
    send(message)

@socketio.on('json')
def handle_json(json):
    send(json, json=True)

@socketio.on('my event')
def handle_my_custom_event(json):
    emit('my response', json)

if __name__ == '__main__':
    socketio.run(app)