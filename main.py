from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import personas_routes, auth_routes, categories_routes, productos_routes

app = FastAPI()

# * para permitir cualquier origen 
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

# * inclusion de las rutas
app.include_router(personas_routes.router, prefix="/personas")
app.include_router(auth_routes.router, prefix="/auth", tags=["auth"])
app.include_router(categories_routes.router, tags=["categories"])
app.include_router(productos_routes.router, tags=["productos"])
