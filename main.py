from fastapi import FastAPI
from src.Routes import all_routes


app = FastAPI()


app.include_router(all_routes.router, prefix="/api")

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)




