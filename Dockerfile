FROM python:3.12.3-bookworm
ENV TZ=Europe/Berlin
ENV DEBIAN_FRONTEND noninteractive

LABEL org.opencontainers.image.description  "Discord Bot for fetching PDF Documents"
LABEL org.opencontainers.image.source     "https://github.com/Katze719/BSZET_IT_BOT"

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
