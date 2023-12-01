import asyncio

import aiohttp


async def send_requests(text: str):
    batch_url = "http://localhost:3000/combined_lid"
    async with aiohttp.ClientSession() as session:
        async with session.post(batch_url, data=text) as response:
            response_data = await response.json()
            print(response_data)


async def main(batch: list[str]):
    coroutines = [send_requests(text) for text in batch]
    results = await asyncio.gather(*coroutines)
    print(results)


if __name__ == "__main__":
    batch = ["This is a test", "This is another test"]
    asyncio.run(main(batch * 100))
