import os
import random

import asyncpraw
from fastapi import FastAPI
from fastapi.responses import RedirectResponse

app = FastAPI()

reddit = asyncpraw.Reddit(user_agent="Redirecttor",
                          client_id=os.getenv("CLIENT_ID"),
                          client_secret=os.getenv("CLIENT_SECRET"),
                          redirect_uri=os.getenv("REDIRECT_URI"))


@app.get("/")
async def root():
    subreddit = await reddit.subreddit(os.getenv("SUBREDDIT", "ScandinavianInterior"))
    hot_entries_gen = subreddit.hot(limit=100)

    random_entry = random.randint(0, 100)
    counter = 0
    async for entry in hot_entries_gen:
        if counter == random_entry:
            return RedirectResponse(entry.url)
        counter += 1
