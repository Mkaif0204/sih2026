import os
import sys
from pathlib import Path
import uvicorn

# Ensure the backend directory is in sys.path
backend_dir = Path(__file__).resolve().parent
if str(backend_dir) not in sys.path:
    sys.path.insert(0, str(backend_dir))

from app.core.config import settings

if __name__ == "__main__":
    print(f"Starting {settings.PROJECT_NAME} on http://localhost:{settings.PORT}")
    print(f"Interactive API Docs available at http://localhost:{settings.PORT}{settings.API_V1_STR}/docs")
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=settings.PORT,
        reload=False
    )
