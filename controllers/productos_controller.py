from fastapi import HTTPException
from db.supabase import supabase_manager 
from models.productos import ProductosCreate, ProductosUpdate, ProductosDelete

# * Crear un producto
def create_producto(producto: ProductosCreate):
    try:
        data = {
            "nombre": producto.nombre,
            "descripcion": producto.descripcion,
            "precio": producto.precio,
            "imagen": producto.imagen,
            
        }
        
        supabase_manager.client.from_("productos").insert(data).execute()  # Asegúrate de que este método sea correcto
        return {"message": "Producto creado correctamente"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
# * Actualizar productos
def update_producto(producto: ProductosUpdate):
    try:
        # * Acutalizar datos 
        data = {
            "nombre": producto.nombre,
            "descripcion": producto.descripcion,
            "precio": producto.precio,
            "imagen": producto.imagen,
        }
        
        supabase_manager.client.from_("productos").update(data).eq("id",producto.id).execute()
        return {"message": "Producto actualizado correctamente"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
# * Eliminar un producto
def delete_producto(producto: ProductosDelete):
    try:
        # * Eliminar datos
        supabase_manager.client.from_("productos").delete().eq("id",producto.id).execute()
        return {"message": "El producto a sido eliminado correctamente"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
