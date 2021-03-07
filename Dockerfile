FROM python:3.7
ENV PYTHONUNBUFFERED 1
RUN mkdir /home/ubuntu
WORKDIR /home/ubuntu
COPY . /home/ubuntu

RUN pip install -r requirements.txt
RUN python manage.py makemigrations
RUN python manage.py migrate
# RUN python manage.py collectstatic

# CMD python manage.py runserver 0.0.0.0:8000
CMD gunicorn --bind 0.0.0.0:8000 config.wsgi:application
