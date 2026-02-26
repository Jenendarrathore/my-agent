import uvicorn
from app.routes.user import router as user_router
from app.core.setup import create_application

# Bootstrap the application using the centralized setup function
app = create_application(router=user_router)

@app.get("/")
async def health_check():
    return {"status": "ok"}

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
