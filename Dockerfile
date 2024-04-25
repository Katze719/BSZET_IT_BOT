FROM python:3.10.13-bookworm
ENV TZ=Europe/Berlin
ENV DEBIAN_FRONTEND noninteractive

LABEL org.opencontainers.image.description DESCRIPTION

RUN set -eux; \
    mkdir /app;

COPY . /app/

RUN set -eux; \
    apt-get update; \
    apt-get install -y \
      pip \
      python3 \
      poppler-utils \
      ghostscript \
      python3-tk \
      libgl1 \
    ;

WORKDIR /app

RUN set -eux; \
    pip3 install -r ./requirements.txt; \
    pip3 install -U table2ascii;
    
CMD ["python3", "./bot.py"]
