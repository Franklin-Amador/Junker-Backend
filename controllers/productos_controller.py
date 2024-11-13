from fastapi import HTTPException
from db.supabase import supabase_manager 
from models.productos import ProductosCreate, ProductosUpdate, ProductosDelete, ProductoRead
from typing import Optional

# * Ver un producto
def get_UnProducto(product_id: ProductoRead):
    try:
        producto = supabase_manager.client.from_("productos").select(
            "*, productos_imagenes(url), productos_categorias(categorias (nombre)), vendedores(calificacion, descripcion, usuarios(nombre, apellido, email))"
            ).eq("id", product_id).single().execute()
        return producto.data
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# * Ver los productos testeo v1     
def get_productos(offset: int, limit: int, categoria: str = None):
    try:
        # Iniciamos la consulta base para los productos
        query = supabase_manager.client.from_("productos").select(
            "*, productos_imagenes(url, orden), productos_categorias(categorias (nombre)), vendedores(calificacion, descripcion, usuarios(nombre, apellido, email))"
        ).eq("productos_imagenes.orden", 0) \
         .range(offset, offset + limit - 1)
        
        # Si se especifica una categoría, aplicar el filtro
        if categoria:
            query = query.eq("productos_categorias.categorias.nombre", categoria)  # Asegúrate de usar eq correctamente

        # Ejecutar la consulta
        productos = query.execute()

        # Retornar los productos obtenidos
        return productos.data
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))



def count_productos():
    try:
        count_result = supabase_manager.client.from_("productos").select("id", count="exact").execute()  # Contar todos los productos
        return count_result.count  # Regresar el total de productos
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# # * Crear un producto
# def create_producto(producto: ProductosCreate):
#     try:
#         data = {
#             "nombre": producto.nombre,
#             "descripcion": producto.descripcion,
#             "precio": producto.precio,
#             "estado_producto": producto.estado_producto,
#             "id_vendedor": producto.id_vendedor,       
#         }
        
#         producto_res = supabase_manager.client.from_("productos").insert(data).execute() 
        
#         if not producto_res.data:
#             raise HTTPException(status_code=400, detail="Error al crear el producto")
        
#         producto_id = producto_res.data[0]["id"]
        
#         imagen_data = [
#             {
#                 "id_producto": producto_id,
#                 "url": url,
#                 "orden": index  # Para mantener el orden de las imágenes
#             }
#             for index, url in enumerate(producto.imagen_url)  # Iterar sobre cada URL
#         ]
        
#         imagen_res = supabase_manager.client.from_("productos_imagenes").insert(imagen_data).execute()
        
#         if not imagen_res.data:
#             raise HTTPException(status_code=400, detail="Error al crear la imagen del producto")
        
#         return {"message": "Producto creado correctamente"}
#     except Exception as e:
#         raise HTTPException(status_code=400, detail=str(e))
    
    
#     # * Crear un producto
def create_producto(producto: ProductosCreate):
    try:
        data_producto = {
            "nombre": producto.nombre,
            "descripcion": producto.descripcion,
            "precio": producto.precio,
            "estado_producto": producto.estado_producto,
            "id_vendedor": producto.id_vendedor,
            "stock": producto.stock,       
        }
        
        producto_res = supabase_manager.client.from_("productos").insert(data_producto).execute() 
        
        if not producto_res.data:
            raise HTTPException(status_code=400, detail="Error al crear el producto")
        
        producto_id = producto_res.data[0]["id"]
        
        imagen_data = [
            {
                "id_producto": producto_id,
                "url": url,
                "orden": index  # Para mantener el orden de las imágenes
            }
            for index, url in enumerate(producto.imagen_url)  # Iterar sobre cada URL
        ]
        
        imagen_res = supabase_manager.client.from_("productos_imagenes").insert(imagen_data).execute()
        
        if not imagen_res.data:
            raise HTTPException(status_code=400, detail="Error al crear la imagen del producto")
        
        
        Producto_categoria = [
                {
                "id_producto": producto_id,
                "id_categoria": producto.id_categoria,
                }
        ]
        
        Producto_categoria_res = supabase_manager.client.from_("productos_categorias").insert(Producto_categoria).execute()
        
        if not Producto_categoria_res.data:
            raise HTTPException(status_code=400, detail="Error al crear el producto y la categoria")
        
        return {"message": "Producto y categoría creados correctamente"}
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
    
