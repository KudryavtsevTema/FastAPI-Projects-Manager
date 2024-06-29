from fastapi import APIRouter, FastAPI
import uvicorn
from routers.project_router import main_project_router
from routers.user_router import secure_router



app = FastAPI()

main_api_router = APIRouter()   
main_api_router.include_router(main_project_router, prefix="/projects", tags=["projects"])
main_api_router.include_router(secure_router, prefix="/auth", tags=["secure"])

app.include_router(main_api_router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)