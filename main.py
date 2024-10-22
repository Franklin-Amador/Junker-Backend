from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import personas_routes, auth_routes

app = FastAPI()



app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return{ "message":"GG" }

app.include_router(personas_routes.router)
app.include_router(auth_routes.router, prefix="/auth", tags=["auth"])