# BSZET_IT_BOT
- [bszet website](https://geschuetzt.bszet.de/index.php?dir=/Schuelerbereich/BS&sort=name)

current username + password:
- username: bsz-et-2324
- password: schulleiter#23

## Usage

invite the bot to your discord via https://discord.com/oauth2/authorize?client_id=1150762234620944464&permissions=8&scope=bot

and type `/activate` in your discord server to activate the bot

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

## Updating the Bot

```sh
docker-compose down
docker pull ghcr.io/katze719/bszet_it_bot:latest
docker-compose up -d
```

# Commands

## Admin Commands

| Command                                   | Description                                      |
|-------------------------------------------|--------------------------------------------------|
| `/activate`                               | Activates the bot                                |
| `/deactivate`                             | Deactivates the bot                              |
| `/deactivate_experimental_features`       | Deactivates experimental features                |
| `/activate_experimental_features`         | Activates experimental features                  |
| `/set <variable_name> <value>`            | Sets the specified variable to the given value   |
| `/reset`                                  | Resets all variables to their default values     |

## User Commands

| Command                                 | Description                                    | Requires Experimental Features to be on |
|-----------------------------------------|------------------------------------------------|--------------------------------|
| `/help`                                 | Displays a help message                        | false                          |
| `/ping`                                 | Checks the bot's responsiveness                | false                          |
| `/plan`                                 | Retrieves the current plan                     | false                          |
| `/get <variable_name>`                  | Retrieves the value of the specified variable  | false                          |
| `/status`                               | Checks if the bot is currently active          | false                          |
| `/feedback <message>`                   | Submits user feedback                          | false                          |
| `/print_parsed_table_experimental`      | Displays the parsed table                      | true                           |
| `/news_experimental`                    | Retrieves the latest news                      | true                           |




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
