FROM python:3.10.13-bookworm
ENV TZ=Europe/Berlin
ENV DEBIAN_FRONTEND noninteractive

LABEL org.opencontainers.image.description DESCRIPTION

RUN set -eux; \
    mkdir /app;

COPY ./bot.py /app/
COPY ./src/compare_pdf.py /app/src/
COPY ./src/document.py /app/src/
COPY ./src/log.py /app/src/
COPY ./src/helpers.py /app/src/
COPY ./src/table_parser.py /app/src/
COPY ./src/settings.py /app/src/
COPY ./requirements.txt /app/


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
