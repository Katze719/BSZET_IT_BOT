# BSZET_IT_BOT
- [bszet website](https://geschuetzt.bszet.de/index.php?dir=/Schuelerbereich/BS&sort=name)

## Run with Docker-Compose

```yml
version: '3'

services:
  schulbot:
    image: ghcr.io/katze719/bszet_it_bot:latest
    restart: always
    environment:
      DISCORD_BOT_TOKEN: ${DISCORD_BOT_TOKEN}
    volumes:
      - ./settings:/settings
```

```sh
mkdir settings
docker-compose up -d
```

## Activate the Bot with the command `/activate`

## Dev Setup

1. Setup venv

```sh
git clone https://github.com/Katze719/BSZET_IT_BOT.git;
cd BSZET_IT_BOT;
python3 -m venv venv;
source ./venv/bin/activate;
pip install -r requirements.txt;
```

2. Run the bot

```sh
export DISCORD_BOT_TOKEN="<my token>"
python3 ./bot.py
```
