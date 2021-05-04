FROM python:3.7
ENV PYTHONUNBUFFERED 1
RUN mkdir /home/ubuntu
WORKDIR /home/ubuntu

RUN apt-get update -y && apt-get install -y libgl1-mesa-dev
COPY download_model.sh /home/ubuntu
RUN sh download_model.sh
COPY requirements.txt /home/ubuntu
RUN python -m venv env
RUN /bin/bash -c "source env/bin/activate"
RUN pip install -r requirements.txt
COPY . /home/ubuntu
RUN python manage.py makemigrations
RUN python manage.py migrate --run-syncdb
RUN python manage.py collectstatic

# CMD python manage.py runserver 0.0.0.0:8000
CMD gunicorn --bind 0.0.0.0:8000 config.wsgi:application
