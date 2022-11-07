# this file demonstrates the use of aiohttp and asyncio as a client to make requests to the server
import asyncio
import aiohttp
import async_timeout


async def fetch(session, url):
    async with async_timeout.timeout(10):
        async with session.get(url) as response:
            return await response.json()


async def main():
    async with aiohttp.ClientSession() as session:
        json = await fetch(session, 'http://time.jsontest.com/')
        print(json)

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
