FROM python:2.7-slim

RUN pip install virtualenv

WORKDIR /app
RUN virtualenv /env
ADD requirements.txt /app/requirements.txt
RUN /env/bin/pip install -r requirements.txt
ADD . /app
ENV SENDER alert.hochudong@gmail.com
ENV PASSWORD_SENDER PTCC@!2o015
ENV NETWORK_PUBLIC_NAME public
EXPOSE 5000

CMD []
ENTRYPOINT ["/env/bin/python", "/app/main.py"]