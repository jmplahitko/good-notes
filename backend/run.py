#!/usr/bin/env python3
"""
Convenience script to run the Good Notes backend server.

Usage:
    python backend/run.py
    
Or with custom host/port:
    python backend/run.py --host 0.0.0.0 --port 8080
"""

import argparse
import uvicorn

from config import get_config


def main():
    parser = argparse.ArgumentParser(description="Run the Good Notes API server")
    parser.add_argument("--host", default="127.0.0.1", help="Host to bind to")
    parser.add_argument("--port", type=int, default=8000, help="Port to bind to")
    parser.add_argument("--reload", action="store_true", help="Enable auto-reload")
    
    args = parser.parse_args()
    
    # Ensure directories exist
    config = get_config()
    config.ensure_directories()
    
    print(f"Starting Good Notes API server...")
    print(f"Notes directory: {config.notes_base_directory}")
    print(f"Action items file: {config.action_items_file}")
    print(f"API URL: http://{args.host}:{args.port}")
    print()
    
    uvicorn.run(
        "main:app",
        host=args.host,
        port=args.port,
        reload=args.reload,
    )


if __name__ == "__main__":
    main()

