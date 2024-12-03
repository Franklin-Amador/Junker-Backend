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
            subquery = supabase_manager.client.from_("productos_categorias")\
                .select("id_producto, categorias!inner(nombre)")\
                .ilike("categorias.nombre", f"%{categoria}%")
            
            result = subquery.execute()
            return [item['id_producto'] for item in result.data] if result.data else []
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))

    @staticmethod
    async def search_by_estado(search_query: str) -> List[int]:
        """Busca productos por estado"""
        try:
            query = supabase_manager.client.from_("productos")\
                .select("id")\
                .ilike("estado_producto", f"%{search_query}%")
            
            result = query.execute()
            return [item['id'] for item in result.data] if result.data else []
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))

    @classmethod
    async def get_productos(
        cls,
        offset: int,
        limit: int,
        filters: ProductFilter,
        search_query: str = "",
        sort_asc: Optional[bool] = None,  # Parámetro para el ordenamiento
    ) -> List[Dict[Any, Any]]:
        try:
        # * Consulta principal
            query = supabase_manager.client.from_("productos")\
                .select(cls.BASE_SELECT)

        # Si hay término de búsqueda, aplicar búsqueda
            if search_query:
                search_query = search_query.strip()
            # Obtener IDs de productos que coinciden con la categoría y estado
                categoria_ids = await cls.get_filtered_product_ids(search_query) if search_query else []
                estado_ids = await cls.search_by_estado(search_query) if search_query else []
            
            # Combinar todos los IDs encontrados y eliminar duplicados
                all_matching_ids = list(set(categoria_ids + estado_ids))
            
            # Construir la consulta para buscar coincidencias
                if all_matching_ids:
                    query = query.or_(
                        f"nombre.ilike.%{search_query}%,id.in.({','.join(map(str, all_matching_ids))})"
                    )
                else:
                    query = query.ilike("nombre", f"%{search_query}%")
        
        # Aplicar filtros si no hay búsqueda o además de la búsqueda
            if filters.categoria and not search_query:
                productos_ids = await cls.get_filtered_product_ids(filters.categoria)
                if not productos_ids:
                    return []
                query = query.in_("id", productos_ids)

        # Aplicar filtros adicionales
            if filters.precio_min is not None:
                query = query.gte("precio", filters.precio_min)
            if filters.precio_max is not None:
                query = query.lte("precio", filters.precio_max)
            if filters.estado:
                query = query.ilike("estado_producto", f"%{filters.estado}%")

        # Aplicar ordenamiento si se especifica
            # Aplicar ordenamiento según el parámetro sort_asc
            if sort_asc is not None:
                order_by = "precio" if sort_asc else "precio.desc"
                query = query.order(order_by)


        # Aplicar paginación
            query = query.range(offset, offset + limit - 1)

        # Ejecutar consulta principal
            result = query.execute()
            productos = result.data if result.data else []

        # Obtener imágenes y categorías en paralelo si hay productos
            if productos:
                productos_ids = [p["id"] for p in productos]

                imagenes_query = supabase_manager.client.from_("productos_imagenes")\
                    .select("id_producto, url")\
                    .in_("id_producto", productos_ids)\
                    .eq("orden", 0)

                categorias_query = supabase_manager.client.from_("productos_categorias")\
                    .select("id_producto, categorias!inner(nombre)")\
                    .in_("id_producto", productos_ids)

            # Ejecutar consultas en paralelo
                imagenes_result = imagenes_query.execute()
                categorias_result = categorias_query.execute()

            # Mapear resultados
                imagenes_map = {img["id_producto"]: img["url"] for img in imagenes_result.data}
                categorias_map = {cat["id_producto"]: cat["categorias"]["nombre"] for cat in categorias_result.data}

            # Construir respuesta final
                productos = [
                    {
                        "id": producto["id"],
                        "nombre": producto["nombre"],
                        "precio": producto["precio"],
                        "categoria": categorias_map.get(producto["id"]),
                        "estado_producto": producto["estado_producto"],
                        "imagen_url": imagenes_map.get(producto["id"])
                    }
                    for producto in productos
                ]

            return productos
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))


    @classmethod
    async def count_productos(cls, filters: ProductFilter, search_query: str = "") -> int:
        """Cuenta el total de productos con filtros y búsqueda aplicados"""
        try:
            query = supabase_manager.client.from_("productos")\
                .select("*", count="exact")

            # Si hay término de búsqueda, aplicar la misma lógica que en get_productos
            if search_query:
                search_query = search_query.strip()
                categoria_ids = await cls.get_filtered_product_ids(search_query)
                estado_ids = await cls.search_by_estado(search_query)
                
                all_matching_ids = list(set(categoria_ids + estado_ids))
                
                if all_matching_ids:
                    query = query.or_(
                        f"nombre.ilike.%{search_query}%,id.in.({','.join(map(str, all_matching_ids))})"
                    )
                else:
                    query = query.ilike("nombre", f"%{search_query}%")
            
            # Aplicar filtros si no hay búsqueda o además de la búsqueda
            if filters.categoria and not search_query:
                productos_ids = await cls.get_filtered_product_ids(filters.categoria)
                if not productos_ids:
                    return 0
                query = query.in_("id", productos_ids)

            # Aplicar filtros adicionales
            if filters.precio_min is not None:
                query = query.gte("precio", filters.precio_min)
            if filters.precio_max is not None:
                query = query.lte("precio", filters.precio_max)
            if filters.estado:
                query = query.ilike("estado_producto", f"%{filters.estado}%")

            result = query.execute()
            return result.count if result.count is not None else 0
            
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
        # Actualiza los datos del producto
        data = {
            "nombre": producto.nombre,
            "descripcion": producto.descripcion,
            "precio": producto.precio,
            "id_vendedor": producto.id_vendedor,
            "estado_producto": producto.estado_producto,
            "stock": producto.stock
        }
        
        producto_update = supabase_manager.client.from_("productos").update(data).eq("id", producto.id).execute()
        
        if not producto_update.data:
            raise HTTPException(status_code=404, detail="Producto no encontrado")
        
        producto_id = producto_update.data[0]["id"]

        # Elimina las imágenes actuales del producto (si es necesario)
        supabase_manager.client.from_("productos_imagenes").delete().eq("id_producto", producto_id).execute()

        # Inserta las nuevas imágenes
        imagen_data = [
            {"id_producto": producto_id, "url": url, "orden": index}
              for index, url in enumerate(producto.imagen_url)
        ]
        
        imagen_res = supabase_manager.client.from_("productos_imagenes").insert(imagen_data).execute()
        
        if not imagen_res.data:
            raise HTTPException(status_code=400, detail="Error al actualizar las imágenes del producto")
        
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
    
