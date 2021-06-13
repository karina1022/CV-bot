FROM python:3.6.9

WORKDIR /app

ADD . /app

# Check DateTime
RUN echo "Acquire::Check-Valid-Until \"false\";\nAcquire::Check-Date \"false\";" | cat > /etc/apt/apt.conf.d/10no--check-valid-until

# Apt
RUN  apt-get update
RUN  apt-get upgrade -y

# Install cmake
RUN apt-get update
RUN apt-get install -y build-essential
RUN apt-get install -y cmake

# Install OpenCV
RUN apt-get install -y unzip
RUN wget -P /usr/local/src/ https://github.com/opencv/opencv/archive/3.4.1.zip
RUN cd /usr/local/src/ && unzip 3.4.1.zip && rm 3.4.1.zip
RUN cd /usr/local/src/opencv-3.4.1/ && mkdir build
RUN cd /usr/local/src/opencv-3.4.1/build && cmake -D CMAKE_INSTALL_TYPE=Release -D CMAKE_INSTALL_PREFIX=/usr/local/ .. && make -j4 && make install

# Install opencv-python
RUN pip install opencv-python

# Requirement
RUN pip3 install -r requirements.txt

# Tensorflow
RUN echo "deb https://packages.cloud.google.com/apt coral-edgetpu-stable main" | tee /etc/apt/sources.list.d/coral-edgetpu.list
RUN curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | apt-key add -
RUN apt-get update
RUN apt-get install -y python3-tflite-runtime
RUN pip3 install --upgrade numpy

CMD python3 TM2_tflite.py --model model.tflite --labels labels.txt
