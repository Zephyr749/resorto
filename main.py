from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from modules.auth import auth_controller
from modules.common.utils import build_response

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_controller.router, prefix="/auth", tags=["auth"])

@app.get("/")
async def root():
    return build_response(False, {}, message="Invalid Route")


