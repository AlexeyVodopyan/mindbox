from fastapi import FastAPI
import uvicorn

from views.views import main_router

app = FastAPI()
app.include_router(main_router)

if __name__ == "__main__":
    uvicorn.run(
        app,
        host="0.0.0.0",
    )
