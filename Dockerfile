FROM almalinux:latest

RUN dnf install -y gcc g++ make python3 python3-pip espeak-ng
RUN yum update -y && yum install -y \
    wget \
    && yum clean all

RUN wget https://developer.download.nvidia.com/compute/cuda/11.8.0/local_installers/cuda_11.8.0_520.61.05_linux.run
RUN sh cuda_11.8.0_520.61.05_linux.run --silent --toolkit --override

ENV PATH=/usr/local/cuda/bin:${PATH}
ENV LD_LIBRARY_PATH=/usr/local/cuda/lib64:${LD_LIBRARY_PATH}

RUN pip3 install Flask gunicorn supervisor torch==2.2.0 torchvision==0.17.0 torchaudio==2.2.0 --index-url https://download.pytorch.org/whl/cu118
RUN pip3 install TTS

WORKDIR /root

COPY . /root/

COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

EXPOSE 5000

#CMD ["supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]
#CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
CMD ["python3", "app.py"]