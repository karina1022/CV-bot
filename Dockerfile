FROM python:3.6.9

WORKDIR /app

ADD . /app

RUN apt-get update && apt-get install -y python3-opencv

RUN pip3 install -r requirements.txt

RUN echo "deb https://packages.cloud.google.com/apt coral-edgetpu-stable main" | tee /etc/apt/sources.list.d/coral-edgetpu.list
RUN curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | apt-key add -
RUN apt-get update
RUN apt-get install -y python3-tflite-runtime

CMD python3 TM2_tflite.py
