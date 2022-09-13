from flask import Flask, render_template, url_for, redirect, request, session, jsonify
import os

app = Flask(__name__, template_folder = os.path.abspath('.'), static_folder = os.path.abspath('.'))
app.config['SECRET_KEY'] = 'AS4FDG5D6F4SDSD'

users = []
last_message = ''
last_message_author = ''

@app.route('/')
def home():
    return render_template('login.html') if not "user" in session else redirect('/chat/')

@app.route('/chat/')
def chat():
    if "user" in session:
        return render_template('chat.html', user=session["user"])
    else:
        return redirect('/')

@app.route('/api/login/')
def login():
    user = request.args.get('user')
    if user is None:
        return 'user parameter is none', 400
    elif len(user) > 16:
        return 400
    elif user in users:
        return 'user already exists', 400
    else:
        session["user"] = user; users.append(user)
        return redirect('/chat/')

@app.route('/api/chat/get/')
def chat_get():
    return last_message_author + ": " + last_message

@app.route('/api/chat/send/', methods=["POST"])
def chat_send():
    global last_message, last_message_author
    if not "user" in session:
        return redirect('/')
    else:
        message = request.args.get('message')
        if message == '' or len(message) > 50:
            return '', 400
        if last_message == message and last_message_author == session["user"]:
            return 'spam is not authorized', 400
        last_message = message; last_message_author = session["user"]
        return '', 204

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=True)
