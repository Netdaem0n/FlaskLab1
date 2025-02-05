import os.path
import logging
from flask import Flask
import captcha
from flask import request, redirect, url_for, render_template, make_response
from uuid import uuid4
from redis import Redis
from werkzeug.utils import secure_filename


app = Flask(__name__)

redis = Redis(host='redis', port=6379)
app.config['UPLOAD_FOLDER'] = r'static/images/userfiles'
logging.basicConfig(level=logging.DEBUG)


@app.route('/', methods=['GET', 'POST'])
def main_page():

    if not request.cookies.get('name'):
        name = str(uuid4())
        # Log the name and path
        app.logger.debug(f"Generating captcha for: {name}")
        text_captcha, text_filename = captcha.file_image_numbers(6, flag='file',
                                                                 filename=name,
                                                                 img_dir='static images captcha',
                                                                 color='#1f7f11')
        redis.set(name, text_captcha)

        text_filename = text_filename.split('static')[-1].replace('\\', '/')

        app.logger.debug(f"Captcha text: {text_captcha}, Captcha file: {text_filename}")

        response = make_response(render_template('login.html', **{'name': name,
                                                                  'myfile': text_filename}))
        response.set_cookie('name', name, max_age=60 * 60 * 24)
        return response

    if not request.cookies.get('captcha'):
        flag = 'no'
    else:
        flag = 'ok'

    if request.method == 'POST':
        # if not request.cookies.get('name') or not request.cookies.get('numbers'):
        #     redirect(url_for('error_page'))
        name = request.cookies.get('name')

        app.logger.debug(f"Captcha POST : {name}, compare: {request.form.get('numbers')} == {redis.get(name).decode('utf-8')}")
        app.logger.debug(f"REDIS KEYS POST : {redis.keys()}")
        app.logger.debug(f"REDIS KEYS POST : {name.encode() in redis.keys()}")

        if name.encode() in redis.keys() and request.form.get('numbers') == redis.get(name).decode('utf-8'):
            response = redirect(url_for('image'))
            response.set_cookie('captcha', 'ok', max_age=60 * 60)
            return response
        else:

            text_captcha, text_filename = captcha.file_image_numbers(6, flag='file',
                                                                     filename=name,
                                                                     img_dir='static images captcha',
                                                                     color='#1f7f11')

            redis.set(name, text_captcha)

            text_filename = text_filename.split('static')[-1].replace('\\', '/')

            app.logger.debug(f"Captcha ERROR text: {text_captcha}, Captcha file: {text_filename}")

            return render_template('login.html', **{'name': request.cookies.get('name'),
                                                    'error': 'Неверный код',
                                                    'captcha': flag, 'myfile': text_filename})

    else:
        name = request.cookies.get('name')

        text_captcha, text_filename = captcha.file_image_numbers(6, flag='file',
                                                                 filename=name,
                                                                 img_dir='static images captcha',
                                                                 color='#1f7f11')

        redis.set(name, text_captcha)

        text_filename = text_filename.split('static')[-1].replace('\\', '/')

        app.logger.debug(f"Captcha SAVED NAME text: {text_captcha}, Captcha file: {text_filename}")

        return render_template('login.html', **{'name': name,
                                                'captcha': flag,
                                                'myfile': text_filename})

@app.route('/image', methods=['GET', 'POST'])
def image():
    if not request.cookies.get('captcha') or request.cookies.get('captcha') != 'ok':
        return redirect(url_for('main_page'))
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(url_for('error_page'))
        file = request.files['file']
        if file:
            filename = secure_filename(file.filename)
            filename = f"{request.cookies.get('name')}.{filename.split('.')[-1]}"
            file.save(f'{app.config["UPLOAD_FOLDER"]}/{filename}')
            response = make_response(render_template('image_file.html',
                                   **{'info': (file.content_length, file.content_type, filename),
                                      'filename': f'static/images/userfiles/{filename}'}))
            response.set_cookie('filetype', filename.split('.')[-1], max_age=60 * 60 * 24)
            return response

    if request.cookies.get('filetype'):
        if os.path.exists(f'{app.config["UPLOAD_FOLDER"]}/{request.cookies.get("name")}.{request.cookies.get("filetype")}'):
            file = f'{app.config["UPLOAD_FOLDER"]}/{request.cookies.get("name")}.{request.cookies.get("filetype")}'
            return render_template('image_file.html', file_old=file)

    return render_template('image_file.html')


@app.route('/error')
@app.errorhandler(404)
def error_page(er):
    return render_template('error_page.html', **{'error': er})

@app.route('/test_redis')
def test_redis_serv():
    redis.incr('hits')
    counter = str(redis.get('hits'),'utf-8')
    return "Welcome to this webapage!, This webpage has been viewed "+counter+" time(s)"


if __name__ == '__main__':
    app.run(debug=True)