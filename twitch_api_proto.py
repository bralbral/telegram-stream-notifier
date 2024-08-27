import asyncio

from pytwitchapi import TwitchAPI

# Укажите здесь ваши Client ID и Client Secret
CLIENT_ID = "your_client_id"
CLIENT_SECRET = "your_client_secret"
STREAMER_NAME = "streamer_name"  # Укажите имя стримера


async def check_stream_status():
    # Инициализация клиента Twitch API
    twitch = TwitchAPI(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)

    # Получение информации о стримере по его имени
    user = await twitch.get_users(logins=[STREAMER_NAME])

    if not user["data"]:
        print("Стример с таким именем не найден.")
        return

    user_id = user["data"][0]["id"]

    # Получение информации о текущем стриме
    stream_info = await twitch.get_streams(user_id=user_id)

    if stream_info["data"]:
        stream = stream_info["data"][0]
        viewers = stream["viewer_count"]
        start_time = stream["started_at"]

        print(f"Стример {STREAMER_NAME} онлайн!")
        print(f"Текущие зрители: {viewers}")
        print(f"Длительность стрима (начало): {start_time}")
    else:
        print(f"Стример {STREAMER_NAME} не в сети.")


async def main():
    # Запуск проверки каждые 60 секунд
    while True:
        await check_stream_status()
        await asyncio.sleep(60)  # Ожидание 60 секунд перед следующей проверкой


if __name__ == "__main__":
    asyncio.run(main())
