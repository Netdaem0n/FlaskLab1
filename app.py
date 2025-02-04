from flask import Flask

app = Flask(__name__)


@app.route('/')
def hello_world():  # put application's code here
    return 'Привет Света!. Это CI/CD! вариант 3.'


if __name__ == '__main__':
    app.run()
