FROM python:2.7

RUN mkdir -p /UNAMS
WORKDIR /UNAMS
COPY . /UNAMS
ADD requirements.txt requirements.txt

RUN apt-get update
RUN apt-get upgrade -y
RUN apt-get install nginx -y
RUN apt-get install supervisor -y
RUN chmod +x /UNAMS/startserver.sh
ADD default  /etc/nginx/sites-available/default


RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN /etc/init.d/nginx restart

CMD sh /UNAMS/startserver.sh

EXPOSE 80
