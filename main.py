import uvicorn
import os
import sys

from src.api import app

sys.path.append(os.path.join(os.path.dirname(__file__)))

if __name__ == "__main__":
    config = uvicorn.Config(app, host="127.0.0.1",
                            port=8000, log_level="info", reload=True)
    server = uvicorn.Server(config)
    server.run()
