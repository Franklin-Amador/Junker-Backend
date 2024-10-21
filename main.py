from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import personas_routes, auth_routes

app = FastAPI()

# Configuración de CORS para permitir que el frontend acceda al backend
origins = [
    "http://localhost:3000",  # Añadir el dominio del frontend (en este caso Next.js)
    "https://your-frontend-domain.com"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return{ "message":"GG" }

app.include_router(personas_routes.router)
app.include_router(auth_routes.router, prefix="/auth", tags=["auth"])