
if __name__ == "__main__":
    import uvicorn
    from core.config import settings
    uvicorn.run(
        "server:app",
        port=settings.API_PORT,
        host=settings.API_HOST,
        reload=True,
        log_level="DEBUG" if settings.DEBUG else "INFO"
    )
