from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from routes import usuarios_routes, auth_routes, categories_routes, productos_routes, carrito_routes, favoritos_routes
from models.user import MailSend, UserCreate, UserLogin

from routes.auth_routes import register, login

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
app.include_router(usuarios_routes.router, prefix="/usuarios")
app.include_router(auth_routes.router, prefix="/auth", tags=["auth"])
app.include_router(categories_routes.router, tags=["categories"])
app.include_router(productos_routes.router, tags=["productos"])
app.include_router(carrito_routes.router, tags=["carrito"])
app.include_router(favoritos_routes.router, tags=["favorito"])

# * Endpoint registro
@app.post("/auth/register")
async def registro(user: UserCreate):
   response =  await register(user)
   return response     

# * Endpoint login
@app.post("/auth/login")
async def loginn(user: UserLogin):
    response = await login(user)
    return response

