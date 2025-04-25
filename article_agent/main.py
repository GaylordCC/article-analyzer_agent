from fastapi import FastAPI
from .routers import article_analyzer_agent, multi_agent_supervisor

app = FastAPI()

app.include_router(article_analyzer_agent.router)
app.include_router(multi_agent_supervisor.router)