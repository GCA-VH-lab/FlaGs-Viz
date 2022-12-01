# FROM ubuntu

# LABEL maintainer="Veda Bojar <veda.bojar@med.lu.se>"

# RUN apt-get update
# RUN apt-get install -y python3 python3-dev python3-pip

# COPY requirements.txt /tmp/requirements.txt
# RUN pip3 install -r /tmp/requirements.txt

# COPY ./ /FlaGs-Viz
# WORKDIR /FlaGs-Viz

# CMD gunicorn --bind 0.0.0.0:80 wsgi


FROM python:3.8

ENV APP_HOME /app
WORKDIR $APP_HOME
COPY . ./

RUN pip install -r requirements.txt

#EXPOSE 8080
EXPOSE $PORT

CMD python app.py
