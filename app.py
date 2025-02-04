from flask import Flask, jsonify, render_template, request

app = Flask(__name__)


@app.route('/')
def hello_world():
    data = request.remote_addr
    return render_template('base.html', **{'ver': '0.1',
                                           'data': data})


if __name__ == '__main__':
    app.run()
