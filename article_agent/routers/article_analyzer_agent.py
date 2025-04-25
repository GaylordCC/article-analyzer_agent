from fastapi import APIRouter

from ..services.article_analyzer_agent_service import ArticleAnalyzerAgent

router = APIRouter(
    tags=["Article Analyzer Agent"]
)

@router.post("/analyze-article")
async def analyze_article():
    sample_text = """
    Anthropic's MCP (Model Context Protocol) is an open-source powerhouse that lets your applications interact effortlessly with APIs across various systems.
    """
    article = ArticleAnalyzerAgent().agent_structure()
    result = article.invoke({"text": sample_text})
    return {"result": result}