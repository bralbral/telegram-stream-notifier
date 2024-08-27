import asyncio

import aiohttp


class TwitchScraper:
    def __init__(self, user_login):
        self.user_login = user_login
        self.session = aiohttp.ClientSession()

    async def is_stream_live(self):
        url = f"https://www.twitch.tv/{self.user_login}"
        async with self.session.get(url) as response:
            if response.status == 200:
                page_content = await response.text()
                # Check for specific text or keywords that indicate the stream is live
                with open("page.html", mode="w") as fh:
                    fh.write(page_content)
                return "isLiveBroadcast" in page_content
            return False

    async def check_stream(self):
        is_live = await self.is_stream_live()
        if is_live:
            print(f"{self.user_login} is live on Twitch!")
        else:
            print(f"{self.user_login} is not live.")

    async def start(self, check_interval=300):
        try:
            while True:
                await self.check_stream()
                await asyncio.sleep(check_interval)
        finally:
            await self.session.close()


# Example usage
async def main():
    user_login = "blackufa"  # Replace with the Twitch username you want to monitor

    scraper = TwitchScraper(user_login)
    await scraper.start(check_interval=300)  # Check every 5 minutes


# Run the script
if __name__ == "__main__":
    asyncio.run(main())
