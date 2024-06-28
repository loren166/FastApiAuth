from fastapi import FastAPI
from app import routers

app = FastAPI()

app.include_router(routers.router, prefix="/users", tags=["users"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host='127.0.0.1', port=3000)
