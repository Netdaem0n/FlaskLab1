FROM python:3.12-slim


WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN mkdir -p static/images/captcha && chmod -R 755 static/images/captcha
RUN mkdir -p static/images/user && chmod -R 755 static/images/user
RUN mkdir -p static/images/userfiles && chmod -R 755 static/images/userfiles

EXPOSE 5000

CMD ["gunicorn", "-w", "2", "-b", "0.0.0.0:5000", "app:app"]