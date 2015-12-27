FROM ubuntu:14.04
MATAINTER baron
RUN pip install -r requirements.txt
RUN python manage.py runserver
