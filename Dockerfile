FROM python:latest


# install gcc and g++ so that liblpclassifier_cv32 can utilize the library
RUN echo 'deb http://deb.debian.org/debian/ sid main' >> /etc/apt/sources.list
RUN apt-get update -y && \
    apt-get install -y \
      gcc-5 \
      g++-5 && \
    rm -rf /var/lib/apt/lists/*

# install cmake
RUN apt-get remove -y cmake
RUN curl -O https://cmake.org/files/v3.8/cmake-3.8.2-Linux-x86_64.sh
RUN sh cmake-3.8.2-Linux-x86_64.sh --skip-license

# install independently cause it takes long time
RUN pip3 install dlib==19.15.0 face-recognition==1.2.2 face-recognition-models==0.3.0

COPY . /app

RUN cd app && pip3 install -r requirements.txt

CMD cd app && python main.py