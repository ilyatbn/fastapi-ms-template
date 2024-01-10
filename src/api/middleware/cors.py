from fastapi.middleware.cors import CORSMiddleware

from core.app_config import config


def add_cors_middleware(app):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=config.CORS_ALLOWED_ORIGINS,
        allow_credentials=config.CORS_ALLOW_CREDENTIALS,
        allow_methods=config.CORS_ALLOWED_METHODS,
        allow_headers=config.CORS_ALLOWED_HEADERS,
    )
