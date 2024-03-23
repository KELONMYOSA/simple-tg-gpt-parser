import pandas as pd
from telethon import TelegramClient
from telethon.errors import ChannelPrivateError

from src.config import settings

client = TelegramClient("anon", settings.TG_API_ID, settings.TG_API_HASH)


async def fetch_posts(channel, limit):
    try:
        posts = []
        async for message in client.iter_messages(channel, limit=limit):
            print(f"Канал - {channel}, ID сообщения - {message.id}")
            if message.text:
                posts.append(message.text)
        return posts
    except ChannelPrivateError:
        print(f"Канал {channel} является частным или ссылка неверна.")
        return []


def get_raw_data():
    sources_df = pd.read_csv("data/sources.csv")
    raw_data = []

    with client:
        for _, row in sources_df.iterrows():
            channel = row["source"]
            depth = row["depth"]
            posts = client.loop.run_until_complete(fetch_posts(channel, depth))

            for post in posts:
                raw_data.append([channel, post])

    raw_df = pd.DataFrame(raw_data, columns=["source", "text"])
    raw_df.to_csv("data/raw_data.csv", index=False)
