from fastapi import HTTPException
from db.supabase import supabase_manager 
from models.productos import ProductosCreate, ProductosUpdate, ProductosDelete, ProductoRead, ProductFilter
from typing import Optional, List, Dict, Any

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
# ! Version test
class ProductQuery:
    """Clase para manejar las consultas de productos"""
    BASE_SELECT = """
        id, precio, nombre, estado_producto
    """

    @staticmethod
    async def get_filtered_product_ids(categoria: str) -> List[int]:
        """Obtiene los IDs de productos filtrados por categoría"""
        try:
            # Subconsulta para obtener id_producto usando una relación directa con id_categoria
            subquery = supabase_manager.client.from_("productos_categorias")\
                .select("id_producto, categorias!inner(nombre)")\
                .eq("categorias.nombre", categoria)
            
            result = subquery.execute()

            # Devolver solo IDs de productos si hay coincidencias
            return [item['id_producto'] for item in result.data] if result.data else []
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))

    @classmethod
    async def get_productos(
        cls,
        offset: int,
        limit: int,
        filters: ProductFilter
    ) -> List[Dict[Any, Any]]:
        """Obtiene productos con filtros aplicados"""
        try:
            # Crear consulta base en productos (solo los campos necesarios)
            query = supabase_manager.client.from_("productos")\
                .select(cls.BASE_SELECT)

            # Aplicar filtro por categoría si existe
            if filters.categoria:
                productos_ids = await cls.get_filtered_product_ids(filters.categoria)
                if not productos_ids:
                    return []  
                query = query.in_("id", productos_ids)

            # Aplicar filtros adicionales (precio, estado, etc.)
            query = filters.apply_filters(query)

            # Aplicar rango
            query = query.range(offset, offset + limit - 1)

            # Ejecutar consulta principal de productos
            result = query.execute()
            productos = result.data if result.data else []

            if productos:
                productos_ids = [p["id"] for p in productos]

                # Obtener imágenes y categorías en paralelo
                imagenes_query = supabase_manager.client.from_("productos_imagenes")\
                    .select("id_producto, url")\
                    .in_("id_producto", productos_ids)\
                    .eq("orden", 0)  # Solo la primera imagen

                categorias_query = supabase_manager.client.from_("productos_categorias")\
                    .select("id_producto, categorias!inner(nombre)")\
                    .in_("id_producto", productos_ids)

                # Ejecutar ambas consultas en paralelo
                imagenes_result = imagenes_query.execute()
                categorias_result = categorias_query.execute()

                # Mapear imágenes y categorías por id_producto
                imagenes_map = {img["id_producto"]: img["url"] for img in imagenes_result.data}
                categorias_map = {cat["id_producto"]: cat["categorias"]["nombre"] for cat in categorias_result.data}

                # Agregar la imagen y la categoría al producto correspondiente
                for producto in productos:
                    producto["imagen_url"] = imagenes_map.get(producto["id"])
                    producto["categoria"] = categorias_map.get(producto["id"])

                # Limpiar los productos para que solo contengan los campos deseados
                productos = [
                    {
                        "id": producto["id"],
                        "nombre": producto["nombre"],
                        "precio": producto["precio"],
                        "categoria": producto["categoria"],
                        "estado_producto": producto["estado_producto"],
                        "imagen_url": producto.get("imagen_url")
                    }
                    for producto in productos
                ]

            return productos
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))

    @classmethod
    async def count_productos(cls, filters: ProductFilter) -> int:
        """Cuenta el total de productos con filtros aplicados"""
        try:
            # Crear consulta base
            query = supabase_manager.client.from_("productos")\
                .select("*", count="exact")

            # Aplicar filtro por categoría si existe
            if filters.categoria:
                productos_ids = await cls.get_filtered_product_ids(filters.categoria)
                if not productos_ids:
                    return 0
                query = query.in_("id", productos_ids)

            # Aplicar filtros adicionales
            query = filters.apply_filters(query)

            result = query.execute()
            return result.count
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
    
