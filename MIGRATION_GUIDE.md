# Миграция с SQLite на PostgreSQL

Это руководство описывает как перейти с SQLite на PostgreSQL для проекта telegram-stream-notifier.

## Требования

- PostgreSQL 12+
- asyncpg (установлен автоматически при `pip install -r requirements.txt`)

## Локальная разработка

### 1. Установка PostgreSQL

**macOS (Homebrew):**
```bash
brew install postgresql
brew services start postgresql
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt-get install postgresql postgresql-contrib
sudo systemctl start postgresql
```

**Docker:**
```bash
docker run --name postgres_notifier \
  -e POSTGRES_PASSWORD=postgres \
  -e POSTGRES_DB=youtube_notifier \
  -p 5432:5432 \
  -v postgres_data:/var/lib/postgresql/data \
  -d postgres:15-alpine
```

### 2. Создание БД и пользователя

```bash
# Подключение к PostgreSQL
psql -U postgres

# SQL команды
CREATE USER youtube_notifier WITH PASSWORD 'your_secure_password';
CREATE DATABASE youtube_notifier OWNER youtube_notifier;
GRANT ALL PRIVILEGES ON DATABASE youtube_notifier TO youtube_notifier;
```

### 3. Установка зависимостей

```bash
pip install -r requirements.txt
```

### 4. Установка переменных окружения

```bash
export DATABASE_HOST=localhost
export DATABASE_PORT=5432
export DATABASE_USER=youtube_notifier
export DATABASE_PASSWORD=your_secure_password
export DATABASE_NAME=youtube_notifier
```

### 5. Инициализация БД

```bash
# Автоматически создаст таблицы при первом запуске
python -m src create-super-user <telegram_id>

# Или запустить приложение
python -m src
```

## Kubernetes развертывание

### 1. Создание Secret для учетных данных БД

```bash
kubectl create secret generic yt-notifier-secrets \
  --from-literal=database.user=youtube_notifier \
  --from-literal=database.password=your_secure_password \
  -n yt-notifier-namespace
```

### 2. Развертывание PostgreSQL (опционально)

Если вы хотите развернуть PostgreSQL в Kubernetes, используйте пример из `deploy/k8s/02_persistent_volume.yaml`.

Или используйте внешний PostgreSQL сервис:
- AWS RDS
- Google Cloud SQL
- Azure Database for PostgreSQL

### 3. Обновление ConfigMap

Отредактируйте `deploy/k8s/01_configmap.yaml` и установите правильные значения для:
- `database.host` - хост PostgreSQL сервера
- `database.port` - порт (обычно 5432)
- `database.name` - название БД

### 4. Развертывание приложения

```bash
kubectl apply -f deploy/k8s/00_namespace.yaml
kubectl apply -f deploy/k8s/01_configmap.yaml
kubectl apply -f deploy/k8s/04_deployment.yaml
```

## Миграция существующих данных из SQLite

Если у вас есть существующая SQLite БД и вы хотите перенести данные:

### 1. Используя pgloader (рекомендуется)

```bash
# Установка
brew install pgloader  # macOS
sudo apt-get install pgloader  # Linux

# Миграция
pgloader sqlite:///youtube-notifier-bot.db postgresql://user:password@localhost/youtube_notifier
```

### 2. Используя Python скрипт

```python
import sqlite3
import asyncpg
import asyncio

async def migrate_sqlite_to_postgres():
    # Подключение к SQLite
    sqlite_conn = sqlite3.connect('youtube-notifier-bot.db')
    sqlite_conn.row_factory = sqlite3.Row
    
    # Подключение к PostgreSQL
    pg_conn = await asyncpg.connect(
        user='youtube_notifier',
        password='password',
        database='youtube_notifier',
        host='localhost',
    )
    
    try:
        # Мигрируем данные
        # ... код миграции ...
        pass
    finally:
        await pg_conn.close()
        sqlite_conn.close()

# Запуск
asyncio.run(migrate_sqlite_to_postgres())
```

## Rollback на SQLite

Если вам нужно вернуться на SQLite:

1. Переключитесь на ветку git перед миграцией или восстановите старый код
2. Переустановите зависимости: `pip install aiosqlite==0.22.1`
3. Обновите переменные окружения:
   ```bash
   export SQLITE_DATABASE_FILE_PATH=youtube-notifier-bot.db
   ```

## Миграции БД (Aerich)

При изменении моделей используйте Aerich для управления миграциями:

```bash
# Создание миграции
aerich migrate --name "описание изменения"

# Применение миграций
aerich upgrade

# История миграций
aerich show
```

## Поиск неисправностей

### Ошибка подключения
```
asyncpg.exceptions.CannotConnectNowError
```
Проверьте:
- PostgreSQL запущен
- Правильные учетные данные в переменных окружения
- Хост и порт доступны

### Ошибка создания таблиц
```
asyncpg.exceptions.UndefinedTableError
```
Убедитесь что БД инициализирована:
```bash
python -m src create-super-user <telegram_id>
```

## Мониторинг БД

Для мониторинга PostgreSQL можно использовать:
- pgAdmin (веб-интерфейс)
- DBeaver (клиент)
- psql (командная строка)

```bash
# Подключение через psql
psql -h localhost -U youtube_notifier -d youtube_notifier
```

## Дополнительные ресурсы

- [Tortoise ORM PostgreSQL документация](https://tortoise-orm.readthedocs.io/en/latest/)
- [Asyncpg документация](https://magicstack.github.io/asyncpg/)
- [PostgreSQL документация](https://www.postgresql.org/docs/)
