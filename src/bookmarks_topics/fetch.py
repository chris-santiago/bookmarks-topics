import asyncio
import typing as T

import aiohttp
import hydra

import bookmarks_topics._common as C


HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
}


async def fetch(session: aiohttp.ClientSession, url: str):
    try:
        async with session.get(url, headers=HEADERS) as response:
            return await response.text()
    except Exception:
        return None


async def fetch_all(urls: T.List[str]):
    connector = aiohttp.TCPConnector(limit_per_host=5, limit=500)
    async with aiohttp.ClientSession(connector=connector) as session:
        results = await asyncio.gather(
            *[fetch(session, url) for url in urls], return_exceptions=False
        )
        return results


@hydra.main(config_path="../../conf", config_name="config", version_base="1.3")
def main(cfg):
    bookmarks_data = C.from_pickle(cfg.html.input_path)
    raw_html = asyncio.run(fetch_all([b.url for b in bookmarks_data]))
    C.to_pickle(raw_html, cfg.html.output_path)


if __name__ == "__main__":
    main()
