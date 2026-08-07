from fastapi import FastAPI
from features.routes import router as api_router

app = FastAPI(title="Home file sharing", docs_url="/api/docs", redoc_url="/api/redoc", openapi_url="/api/openapi.json", swagger_ui_oauth2_redirect_url="/api/docs/oauth2-redirect")

app.include_router(api_router)

@app.get("/api")
def root():
    return "Hello, this is a home-based web service for file sharing."
