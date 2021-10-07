from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def earth():
    return render_template('main.html')


@app.route('/socket')
def socket():
    return render_template('socket.html')


@app.route('/debug')
def debug():
    return render_template('debug.html')
