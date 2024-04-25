# SchulBot

- [bszet website](https://geschuetzt.bszet.de/index.php?dir=/Schuelerbereich/BS&sort=name)
bsz-et-2324
schulleiter#23

## Run with Docker

1. pull image
```sh
docker pull ghcr.io/katze719/schulbot:latest
```

2. run docker container with `-d`

```sh
docker run -d ghcr.io/katze719/schulbot:latest
```

## Dev Setup

1. clone project

```sh
git clone https://github.com/Katze719/SchulBot.git
```

2. cd in dir

```sh
cd SchulBot
```

3. create venv

```sh
python -m venv venv
```

4. activate venv

**Windows**
```sh
.\venv\Scripts\activate
```
**macOS and Linux**
```sh
source ./venv/bin/activate
```

5. install dependencies

```sh
pip install -r requirements.txt
```

6. install poppler (preferred to use linux)

**Linux**
```sh
sudo apt-get install poppler-utils
```

**Windows**
Download the latest Release of poppler [here](https://github.com/oschwartz10612/poppler-windows/releases)
and change the python line
```python
images = convert_from_path(f"{file_name}.pdf")
```
to
```python
images = convert_from_path(f"{file_name}.pdf", poppler_path=r'C:\path\to\poppler-23.08.0\Library\bin')
```


## How to Run the Bot

```sh
python3 ./bot.py
```
