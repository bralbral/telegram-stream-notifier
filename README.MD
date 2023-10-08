# telegram-youtube-notifier-bot

Simple Youtube LiveStreams notifier in telegram based on [youtube-dlp](https://github.com/yt-dlp/yt-dlp) and  [aiogram](https://github.com/aiogram/aiogram) .

Use this bot to receive periodic reports on live broadcasts on YouTube and generate and send the report to telegram. 

## Deploy

### Install from source

> Tested on Ubuntu 22.04, python 3.11

Just copy source code:

`git clone https://github.com/bralbral/telegram-youtube-notifier.git`

Install requirements:

`pip intall -r requirements.txt`

Fill [config.yml](./deploy/example.config.yaml) and place it to root dir. (In parent dir to `src`)

Run:

`python3 -m src`

### Install with Docker

> Stable release with `main` tag on [dockerhub](https://hub.docker.com/r/bral1488/telegram-youtube-notifier/tags)

Just copy [docker-compose.yml](./deploy/example.docker-compose.yml) and fill in  [config.yaml](./deploy/example.config.yaml).

Run containers:

`docker-compose up -d` or if you have new docker `docker compose up -d`

Of course, you can build image yourself:

Just copy source code:

`git clone https://github.com/bralbral/telegram-youtube-notifier.git`

and build docker image:

`docker build -t <your_image_name>:<your_tag_name>`

And use this image with [docker-compose.yml](./deploy/example.docker-compose.yml) from `deploy` dir.

## Hosting
You can rent a server from various hosters, for example from [Aeza](https://aeza.net/?ref=380831).

>*By registering via the [link](https://aeza.net/?ref=380831) you will support the project and receive a 15% bonus on your balance, which will be valid for 24 hours.*

The bot will require the simplest VDS, in rubles this is approximately 100-200 for promotional offers, or about 500 rubles per month.

## Develop and Contribute

Feel free to create issue or pull request.

For development, you should install the requirements from [requirements_dev.txt](./requirements_dev.txt)

`pip intall -r requirements_dev.txt`

Use [pre-commit.sh](./pre-commit.sh) before commit.
