from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from modules.auth import auth_controller
from modules.booking import booking_controller, admin_controller, payment_controller
from modules.common.utils import build_response

app = FastAPI(
    title="Resorto API",
    description="Booking system for picnic resort with bedrooms",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

# Auth routes
app.include_router(auth_controller.router, prefix='/auth', tags=['auth'])

# Booking routes (public and user endpoints)
app.include_router(booking_controller.router)

# Admin routes
app.include_router(admin_controller.router)

# Payment routes
app.include_router(payment_controller.router)

@app.get('/')
async def root():
    return {
        'name': 'Resorto API',
        'version': '1.0.0',
        'docs': '/docs',
        'status': 'running'
    }


