from fastapi import HTTPException
from db.supabase import supabase_manager 
from models.productos import ProductosCreate, ProductosUpdate, ProductosDelete, ProductoRead

# * Ver un producto
def get_UnProducto(product_id: ProductoRead):
    try:
        producto = supabase_manager.client.from_("productos").select(
            "*, productos_imagenes(url), productos_categorias(categorias (nombre)), vendedores(calificacion, descripcion, usuarios(nombre, apellido, email))"
            ).eq("id", product_id).single().execute()
        return producto.data
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# * Ver los productos
def get_productos():
    try:
        productos = supabase_manager.client.from_("productos").select(
            "*, productos_imagenes(url), productos_categorias(categorias (nombre)), vendedores(calificacion, descripcion, usuarios(nombre, apellido, email))").execute()
        return productos.data
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# * Crear un producto
def create_producto(producto: ProductosCreate):
    try:
        data = {
            "nombre": producto.nombre,
            "descripcion": producto.descripcion,
            "precio": producto.precio,
            "id_vendedor": producto.id_vendedor,       
        }
        
        producto_res = supabase_manager.client.from_("productos").insert(data).execute() 
        
        producto_id = producto_res.data[0]["id"]
        
        imagen_data = {
            "id_producto": producto_id,
            "url": producto.imagen_url 
        }
        
        imagen_res = supabase_manager.client.from_("productos_imagenes").insert(imagen_data).execute()
        
        if not imagen_res.data:
            raise HTTPException(status_code=400, detail="Error al crear la imagen del producto")
        
        return {"message": "Producto creado correctamente"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
# * Actualizar productos
def update_producto(producto: ProductosUpdate):
    try:
        data = {
            "nombre": producto.nombre,
            "descripcion": producto.descripcion,
            "precio": producto.precio,
            "id_vendedor": producto.id_vendedor,
        }
        
        producto_update = supabase_manager.client.from_("productos").update(data).eq("id",producto.id).execute()
       
        producto_id = producto_update.data[0]["id"]
       
        imagen_data = {
        "id_producto": producto_id,
        "url": producto.imagen_url 
        }
        
        imagen_res = supabase_manager.client.from_("productos_imagenes").insert(imagen_data).execute()
        
        if not imagen_res.data:
            raise HTTPException(status_code=400, detail="Error al actualizar la imagen del producto")
        
       
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
    
