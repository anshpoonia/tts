FROM almalinux:latest

RUN dnf install -y gcc g++ make python3 python3-pip espeak-ng

WORKDIR /root

COPY . /root/

RUN pip3 install llvmlite --ignore-installed
RUN pip3 install TTS
RUN pip3 install Flask


EXPOSE 5000

CMD ["python3", "app.py"]