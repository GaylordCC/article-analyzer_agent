from fastapi import FastAPI
from .routers import article_analyzer_agent

app = FastAPI()

app.include_router(article_analyzer_agent.router)