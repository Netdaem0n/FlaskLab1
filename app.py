from flask import Flask, jsonify, render_template, request, url_for

app = Flask(__name__)
ver = "0.2alfa"  # Определяем ver здесь!
app.config['APPLICATION_ROOT'] = '/lab1'

@app.route('/')
def index():
    data = request.remote_addr
    return render_template('index.html', **{'ver': ver,
                                           'data': data})

@app.route('/about')
def about():
    data = request.remote_addr
    return render_template('about.html', **{'ver': ver,
                                           'data': data})

@app.route('/test')
def test():
    data = request.remote_addr
    return render_template('test.html', **{'ver': ver,
                                           'data': data})

if __name__ == '__main__':
    app.run()
