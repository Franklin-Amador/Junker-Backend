from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from routes import usuarios_routes, auth_routes, categories_routes, productos_routes, carrito_routes
from models.user import MailSend, UserCreate

from utils.sendmail import welcome_email
from routes.auth_routes import register

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

@app.post("/bienvenida")
async def bienvenida(request: MailSend):
    result = await welcome_email(request.email, request.password)
    if not result["success"]:
        raise HTTPException(status_code=400, detail=result["message"])
    return result

# * Endpoint registro
@app.post("/auth/register")
async def registro(user: UserCreate):
   response =  await register(user)
   return response     



