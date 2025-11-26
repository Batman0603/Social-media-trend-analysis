# Entry point for running with 'python main.py'
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=9000, reload=True)
from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse
import httpx
import os
import json
import asyncio

# MCP Server for Social Media Trend Analysis
app = FastAPI(title="MCP Server for Social Media Trend Analysis")

# The FastAPI app is assumed to be running locally on this port
FASTAPI_URL = os.getenv("FASTAPI_URL", "http://127.0.0.1:8000")



# Root endpoint now returns a minimal SSE stream for Cline compatibility
from fastapi.responses import StreamingResponse
import time


import asyncio
async def sse_hello():
    while True:
        yield f"data: {json.dumps({'message': 'MCP Server is running!'})}\n\n"
        await asyncio.sleep(5)

@app.get("/")
async def root():
    return StreamingResponse(sse_hello(), media_type="text/event-stream")


# -------------------------------
# JSON endpoint (for normal usage)
# -------------------------------
@app.post("/query")
async def query_router(request: Request):
    data = await request.json()
    user_query = data.get("query", "")

    async with httpx.AsyncClient() as client:
        if "hashtag" in user_query.lower():
            response = await client.get(f"{FASTAPI_URL}/hashtags")
            return {"result": response.json()}

        elif "comment" in user_query.lower():
            response = await client.get(f"{FASTAPI_URL}/comments")
            return {"result": response.json()}

        elif "user" in user_query.lower():
            response = await client.get(f"{FASTAPI_URL}/users")
            return {"result": response.json()}

        else:
            return {"error": "Query not understood. Please mention hashtag, comment, or user."}


# -----------------------------------
# SSE endpoint (for Clime connection)
# -----------------------------------
async def event_stream(user_query: str):
    async with httpx.AsyncClient() as client:
        if "hashtag" in user_query.lower():
            response = await client.get(f"{FASTAPI_URL}/hashtags")
            result = response.json()

        elif "comment" in user_query.lower():
            response = await client.get(f"{FASTAPI_URL}/comments")
            result = response.json()

        elif "user" in user_query.lower():
            response = await client.get(f"{FASTAPI_URL}/users")
            result = response.json()

        else:
            result = {"error": "Query not understood. Please mention hashtag, comment, or user."}

    # Stream as SSE
    yield f"data: {json.dumps(result)}\n\n"
    await asyncio.sleep(0.1)


from fastapi import Query
from fastapi import Request
from fastapi import APIRouter

from fastapi.responses import StreamingResponse

from fastapi import Request, Query
from fastapi.routing import APIRoute

@app.api_route("/sse", methods=["GET", "POST"])
async def sse_router(request: Request, query: str = Query(None)):
    if request.method == "POST":
        try:
            data = await request.json()
            user_query = data.get("query", "")
        except Exception:
            user_query = ""
    else:
        user_query = query or ""
    return StreamingResponse(event_stream(user_query), media_type="text/event-stream")
