# BSZET_IT_BOT
- [bszet website](https://geschuetzt.bszet.de/index.php?dir=/Schuelerbereich/BS&sort=name)

current username + password:
- username: bsz-et-2324
- password: schulleiter#23

## Using the Bot

invite the bot to your discord via https://discord.com/oauth2/authorize?client_id=1150762234620944464&permissions=8&scope=bot

and activate him with `/activate`

## Self-Hosting with Docker-Compose

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
