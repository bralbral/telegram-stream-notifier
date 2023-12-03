if [[ ! $1 =~ ^[0-9]+$ ]]; then
  echo "You need to create a superuser. Enter its telegram_id. This must be an integer number, for example: 1234567890"
  exit 1
fi
export TELEGRAM_ID=$1
echo "Run dry-run container"
docker compose -f docker-compose-dry-run.yml up
echo "Sleeping"
sleep 5
docker cp dry-run:/app/youtube-notifier-bot.db .
docker rm -f dry-run

