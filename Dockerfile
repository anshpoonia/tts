FROM almalinux:latest

RUN dnf install -y gcc g++ make python3 python3-pip espeak-ng
RUN yum update -y && yum install -y \
    wget \
    && yum clean all

RUN pip3 install Flask gunicorn supervisor
RUN pip3 install torch==2.1.0+cu118 torchvision==0.16.0+cu118 torchaudio==2.1.0+cu118 --index-url https://download.pytorch.org/whl/cu118
RUN pip3 install TTS

WORKDIR /root

COPY . /root/

COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

EXPOSE 5000

#CMD ["supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]
#CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
#CMD ["python3", "app.py"]