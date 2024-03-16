FROM almalinux:latest

RUN dnf install -y gcc g++ make python3 python3-pip espeak-ng
RUN yum update -y && yum install -y \
    wget \
    && yum clean all

RUN wget https://developer.download.nvidia.com/compute/cuda/11.8.0/local_installers/cuda_11.8.0_520.61.05_linux.run
RUN sh cuda_11.8.0_520.61.05_linux.run --silent --toolkit --override

ENV PATH=/usr/local/cuda/bin:${PATH}
ENV LD_LIBRARY_PATH=/usr/local/cuda/lib64:${LD_LIBRARY_PATH}

RUN pip3 install TTS
RUN pip3 install Flask gunicorn supervisor

WORKDIR /root

COPY . /root/

COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

EXPOSE 5000

CMD ["supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]