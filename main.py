import uvicorn
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__)))

if __name__ == "__main__":
    """ 
    os.environ["DB_HOST"] = "127.0.0.1"
    os.environ["DB_USER"] = "root"
    os.environ["DB_PSWD"] = "Adivinala1."
    os.environ["DB"] = "Floppotron"
    """
    
    environ = ["DB_HOST","DB_USER","DB_PSWD","DB"]
    for var in environ:
        if not os.getenv(var):
            raise Exception(f"Error: {var} no encontrado en variables de entorno")
    
    from src.api import app
    
    config = uvicorn.Config(app, host="127.0.0.1",
                            port=8000, log_level="info", reload=True)
    server = uvicorn.Server(config)
    server.run()
