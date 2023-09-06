[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)


## Подготовка к запуску
Скопировать [файл конфигурации](example.config.yaml) и заполнить его.

```console
$ cp example.config.yaml config.yaml
```

## Контрибьютинг

  Установка зависимостей для разработки

   ```console
   $ pip install -r requirements_dev.txt
   ```

  Обязательно, перед коммитом нужно выполнять:
  
   ```console
   $ bash pre-commit.sh
   ```

## Загрузить последний собранный DOCKER-IMAGE

### Login
docker login  registry.thunder.io/top/dev/seeker_bot -u docker -p glpat-acfx4W4xzhcsgWMMRBmb

### Pull
docker pull registry.thunder.io/top/dev/seeker_bot:latest