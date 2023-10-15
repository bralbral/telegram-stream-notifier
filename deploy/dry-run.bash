echo "Run dry-run container"
docker compose -f docker-compose-dry-run.yml up
echo "Sleeping"
sleep 15
docker cp dry-run:/app/youtube-notifier-bot.db .
docker rm -f dry-run

