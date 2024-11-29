from fastapi import APIRouter
from controllers.favoritos_controller import get_favoritos, create_favoritos, update_favoritos, delete_favoritos
from models.favoritos import FavoritoCreate, FavoritoUpdate

router = APIRouter()

@router.get("/favorito/{usuario_id}")
async def obtener_favorito(usuario_id: str): 
    favoritos = get_favoritos(usuario_id)  
    return  favoritos
     
@router.post("/favorito")
async def post_favoritos(favorito: FavoritoCreate):
    return create_favoritos(favorito)

@router.put("/favorito")
async def put_favorito(favorito: FavoritoUpdate):
    return update_favoritos(favorito)

@router.delete("/usuario/{usuario_id}/producto/{producto_id}")
async def borrar_favorito(usuario_id: str, producto_id: str):
    return delete_favoritos(usuario_id , producto_id)

    