"""
Good Notes - FastAPI Backend

A desktop note-taking application backend that stores notes as markdown files
and action items in a JSON file.
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .config import get_config
from .api import notes, action_items, settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan handler for startup/shutdown events."""
    # Startup: ensure directories exist
    config = get_config()
    config.ensure_directories()
    
    print(f"Good Notes API starting...")
    print(f"Notes directory: {config.notes_base_directory}")
    print(f"Action items file: {config.action_items_file}")
    
    yield
    
    # Shutdown
    print("Good Notes API shutting down...")


def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""
    config = get_config()
    
    app = FastAPI(
        title="Good Notes API",
        description="Backend API for the Good Notes desktop application",
        version="1.0.0",
        lifespan=lifespan,
    )
    
    # Configure CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=config.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Include API routers
    app.include_router(notes.router, prefix=config.api_prefix)
    app.include_router(action_items.router, prefix=config.api_prefix)
    app.include_router(settings.router, prefix=config.api_prefix)
    
    @app.get("/")
    async def root():
        """Root endpoint for health check."""
        return {
            "name": "Good Notes API",
            "version": "1.0.0",
            "status": "running",
        }
    
    @app.get("/health")
    async def health_check():
        """Health check endpoint."""
        return {"status": "healthy"}
    
    return app


# Create the application instance
app = create_app()


if __name__ == "__main__":
    import uvicorn
    
    config = get_config()
    uvicorn.run(
        "backend.main:app",
        host=config.api_host,
        port=config.api_port,
        reload=True,
    )

