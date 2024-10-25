# School Blog API

This is a FastAPI application that provides CRUD operations for managing blog posts in a "School Blog" context.
The API connects to MongoDB Atlas to store posts, and the endpoints support creating, retrieving, updating, and deleting blog posts based on criteria like title or author.

## Features

- **MongoDB Atlas Connection**: Connects to MongoDB Atlas using `motor` (async driver).
- **CRUD Operations**: Create, read, update, and delete blog posts.
- **Flexible Filtering**: Search and modify posts based on title and author filters.

## Prerequisites

- Python 3.8+
- MongoDB Atlas account and database
- `motor`, `pydantic`, `fastapi`, and `uvicorn` installed

