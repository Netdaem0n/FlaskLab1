from flask import Flask, jsonify, render_template, request, url_for

app = Flask(__name__)
app.config['APPLICATION_ROOT'] = '/lab1'

@app.route('/')
def index():
    data = request.remote_addr
    return render_template('index.html', **{'ver': '0.1',
                                           'data': data})

@app.route('/about')
def about():
    data = request.remote_addr
    return render_template('about.html', **{'ver': '0.2',
                                           'data': data})

@app.route('/test')
def test():
    data = request.remote_addr
    return render_template('test.html', **{'ver': '0.1',
                                           'data': data})

if __name__ == '__main__':
    app.run()
