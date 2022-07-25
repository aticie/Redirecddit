import os
import random

import asyncpraw
from fastapi import FastAPI
from fastapi.responses import RedirectResponse

import motor.motor_asyncio

# Create FastAPI Server
app = FastAPI()

# Create Reddit Client
reddit = asyncpraw.Reddit(user_agent="Redirecttor",
                          client_id=os.getenv("CLIENT_ID"),
                          client_secret=os.getenv("CLIENT_SECRET"),
                          redirect_uri="http://localhost")

# Connect to MongoDB to fetch the subreddit
conn_str = os.getenv("MONGO_URL")
mongoclient = motor.motor_asyncio.AsyncIOMotorClient(conn_str, serverSelectionTimeoutMS=5000)

@app.get("/")
async def root():
    # Get the subreddit name from MongoDB
    test_collection = mongoclient.test.test
    doc = await test_collection.find_one()
    subreddit_name = doc["subreddit"]

    # Search the top 25 posts in subreddit
    subreddit = await reddit.subreddit(subreddit_name)
    hot_entries_gen = subreddit.hot(limit=25)

    # Select random entry within 25 posts
    random_entry = random.randint(0, 25)
    counter = 0
    async for entry in hot_entries_gen:
        if counter == random_entry:
            return RedirectResponse(entry.url)
        counter += 1
