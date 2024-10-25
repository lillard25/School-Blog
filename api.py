import uvicorn
from fastapi import FastAPI, HTTPException, status, Query
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

app = FastAPI(title="School Blog APIs")

# MongoDB Atlas Connection
MONGO_URL = "mongodb+srv://aditya:12345@cluster0.no8kke7.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = AsyncIOMotorClient(MONGO_URL)
db = client["school_blog"]


# Base Model Definitions
class PostModel(BaseModel):
    title: str = Field("title", min_length=3, max_length=100)
    content: str = Field("content of the blog", min_length=10)
    author: str = Field("author", min_length=3, max_length=50)
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow)


class UpdatePostModel(BaseModel):
    title: Optional[str] = Field("title", min_length=3, max_length=100)
    content: Optional[str] = Field("content of the blog", min_length=10)
    author: Optional[str] = Field("author", min_length=3, max_length=50)


# Utility function to format MongoDB documents
def format_post(post):
    if post:
        post["_id"] = str(post["_id"])
    return post


# Routes
@app.post("/posts/", status_code=status.HTTP_201_CREATED)
async def create_post(post: PostModel):
    new_post = await db["posts"].insert_one(post.dict())
    created_post = await db["posts"].find_one({"_id": new_post.inserted_id})
    return format_post(created_post)


@app.get("/posts/")
async def get_post(title: Optional[str] = Query(None), author: Optional[str] = Query(None)):
    filter_query = {}
    if title:
        filter_query["title"] = title
    if author:
        filter_query["author"] = author
    posts = await db["posts"].find(filter_query).to_list(100)
    if not posts:
        raise HTTPException(status_code=404, detail="Post not found")
    return [format_post(post) for post in posts]


@app.put("/posts/")
async def update_post(title: Optional[str] = Query(None), author: Optional[str] = Query(None),
                      post: UpdatePostModel = None):
    filter_query = {}
    if title:
        filter_query["title"] = title
    if author:
        filter_query["author"] = author
    if not filter_query:
        raise HTTPException(status_code=400, detail="Specify a title or author to update.")

    update_data = {k: v for k, v in post.dict().items() if v is not None}
    if update_data:
        result = await db["posts"].update_many(filter_query, {"$set": update_data})
        if result.modified_count == 0:
            raise HTTPException(status_code=404, detail="Post not found for the given criteria")
        return {"detail": f"{result.modified_count} post(s) updated successfully"}
    return {"detail": "No updates provided"}


@app.delete("/posts/")
async def delete_post(title: Optional[str] = Query(None), author: Optional[str] = Query(None)):
    filter_query = {}
    if title:
        filter_query["title"] = title
    if author:
        filter_query["author"] = author
    if not filter_query:
        raise HTTPException(status_code=400, detail="Specify a title or author to delete.")

    result = await db["posts"].delete_many(filter_query)
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Post not found for the given criteria")
    return {"detail": f"{result.deleted_count} post(s) deleted successfully"}


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8080, log_level="info")
