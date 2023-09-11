from fastapi import FastAPI
from fastapi.responses import PlainTextResponse

from src.user.router import router as router_user
from src.auth.router import router as router_auth


app = FastAPI()


@app.get("/", response_class=PlainTextResponse)
async def main():
    return "Hello World"

app.include_router(router_user)
app.include_router(router_auth)
