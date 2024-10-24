from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.parsers import (
  MultiPartParser,
  FormParser,
)
from utils.pagination import Pagination
from rest_framework.pagination import PageNumberPagination
from django.http import Http404
from .models import (
  CategoryModel,
  ProductModel,
)
from .serializers import (
  CategorySerializer,
  ProductSerializer,
)
from drf_yasg.utils import swagger_auto_schema        # schema para el swagger
from drf_yasg import openapi
from autentication.permissions import (
  IsAuthenticated,
  IsAdmin,
  IsSellerOrAdmin
)

CATEGORY_TAG = 'Categoria de productos'
PRODUCT_TAG = 'Productos'


#------------------------------------------------------------------------------
###                       CRUD PARA CATEGORIAS                              ###
# ----------------------------------------------------------------------------- 

# Lista de categorias
class ListCategoryView(generics.ListAPIView):
  queryset = CategoryModel.objects.all()
  serializer_class = CategorySerializer

  @swagger_auto_schema(tags=[ CATEGORY_TAG ])
  def get(self, request, *args, **kwargs):
    """ Lista de Categorias: metodo get """
    response = super().get(request, *args, **kwargs)
    return Response({
      'message': 'Categorias listadas exitosamente',
      'data': response.data
    }, status=status.HTTP_200_OK
  )

# Crea una nueva categoria
class CreateCategoryView(generics.CreateAPIView):
  serializer_class = CategorySerializer
  permission_classes = [IsAuthenticated, IsAdmin]

  @swagger_auto_schema(tags=[ CATEGORY_TAG ])
  def post(self, request, *args, **kwargs):
    """ Crea una nueva categoria: metodo post """
    response = super().post(request, *args, **kwargs)
    return Response({
      'message': 'Categoria creada exitosamente',
      'data': response.data
      }, status=status.HTTP_201_CREATED
  )

# Actualiza una categoria
class UpdateCategoryView(generics.UpdateAPIView):
  queryset = CategoryModel.objects.all()
  serializer_class = CategorySerializer
  permission_classes = [IsAuthenticated, IsAdmin]

  @swagger_auto_schema(tags=[ CATEGORY_TAG ])
  def put(self, request, *args, **kwargs):
    """ Actualiza una categoria: metodo put """
    try:
      response = super().put(request, *args, **kwargs)
      return Response({
        'message': 'Categoria actualizada exitosamente',
        'data': response.data
        }, status=status.HTTP_200_OK
      )
    except Http404:
      return Response({
        'message': 'Categoria no encontrada',
        }, status=status.HTTP_404_NOT_FOUND)

  @swagger_auto_schema(tags=[ CATEGORY_TAG ])
  def patch(self, request, *args, **kwargs):
    """ Actualiza una categoria: metodo patch """
    try:
      response = super().partial_update(request, *args, **kwargs)
      return Response({
        'message': 'Categoria actualizada exitosamente',
        'data': response.data
        }, status=status.HTTP_200_OK)
    except Http404:
      return Response({
        'message': 'Categoria no encontrada',
        }, status=status.HTTP_404_NOT_FOUND)

# Elimina una categoria
class DeleteCategoryView(generics.DestroyAPIView):
  queryset = CategoryModel.objects.all()
  permission_classes = [IsAuthenticated, IsAdmin]

  @swagger_auto_schema(tags=[ CATEGORY_TAG ])
  def delete(self, request, *args, **kwargs):
    """ Elimina una categoria: metodo delete """
    try:
      category = self.get_object()
      category.status = False
      category.save()
      return Response({
        'message': 'Categoria eliminada exitosamente',
        }, status=status.HTTP_200_OK)
    except Http404:
      return Response({
        'message': 'Categoria no encontrada',
        }, status=status.HTTP_404_NOT_FOUND)
    
#------------------------------------------------------------------------------
###                             PRODUCTOS                                   ###
# ----------------------------------------------------------------------------- 
  
# Lista de productos
class ListProductView(generics.ListAPIView):
  #queryset = ProductModel.objects.all()   no es necesario porque se filtra en la funcion get_queryset
  queryset = ProductModel.objects.all()
  serializer_class = ProductSerializer
  pagination_class = Pagination
  permission_classes = [IsAuthenticated, IsSellerOrAdmin]

  # order_param = openapi.Parameter(
  #   'order',
  #   openapi.IN_QUERY,
  #   type=openapi.TYPE_STRING,
  #   enum=['ASC', 'DESC'],
  #   required=False,
  #   description='Orden de la lista de productos'
  # )

  # def get_queryset(self):
  #   queryset = ProductModel.objects.filter(status='ACTIVE').order_by('-id')
  #   return queryset

  @swagger_auto_schema(tags=[ PRODUCT_TAG ])
  def get(self, request, *args, **kwargs):
    """ Lista de productos: metodo get """
    response = super().get(request, *args, **kwargs)

    return Response({
      'message': 'Productos listados exitosamente',
      'data': response.data['results'],
      'count': response.data['count'],
      'next': response.data['next'],
      'previous': response.data['previous']
      }, status=status.HTTP_200_OK)

#Lista de productos activos
class ListActiveProductView(generics.ListAPIView):
  serializer_class = ProductSerializer
  pagination_class = Pagination

  def get_queryset(self):
    queryset = ProductModel.objects.filter(status='ACTIVE').order_by('name')
    return queryset
  
  @swagger_auto_schema(tags=[ PRODUCT_TAG ])
  def get(self, request, *args, **kwargs):
    """ Lista de productos activos: metodo get """
    response = super().get(request, *args, **kwargs)
    return Response({
      'message': 'Productos listados exitosamente',
      'data': response.data['results'],
      'count': response.data['count'],
      'next': response.data['next'],
      'previous': response.data['previous']
      }, status=status.HTTP_200_OK)
  
# Busca productos por nombre
class SearchProductView(generics.ListAPIView):
  serializer_class = ProductSerializer
  pagination_class = Pagination

  def get_queryset(self):
    queryset = ProductModel.objects.filter(name__icontains=self.kwargs['name']).order_by('-id')
    return queryset

  @swagger_auto_schema(tags=[ PRODUCT_TAG ])
  def get(self, request, *args, **kwargs):
    """ Buscar productos por el nombre: metodo get """
    response = super().get(request, *args, **kwargs)

    return Response({
      'message': 'Productos listados exitosamente',
      'data': response.data['results'],
      'count': response.data['count'],
      'next': response.data['next'],
      'previous': response.data['previous']
      }, status=status.HTTP_200_OK) 

# Crea un producto
class CreateProductView(generics.CreateAPIView):
  serializer_class = ProductSerializer
  #permission_classes = [IsAuthenticated, IsAdmin]
  parser_classes = [MultiPartParser, FormParser]

  # Parametro para subir desde SWAGER la imagen del producto (formuDATA) 
  image_param = openapi.Parameter(
    'image',
    openapi.IN_FORM,
    type=openapi.TYPE_FILE,
    required=True,
    description='Imagen del producto'
  )

  @swagger_auto_schema(
    tags=[ PRODUCT_TAG ],
    manual_parameters=[ image_param ],
    consumes=['multipart/form-data']
  )
  def post(self, request, *args, **kwargs):
    """ Crea un producto: metodo post """
    response = super().post(request, *args, **kwargs)
    return Response({
      'message': 'Producto creado exitosamente',
      'data': response.data
      }, status=status.HTTP_201_CREATED)

# Actualiza un producto
class UpdateProductView(generics.UpdateAPIView):
  queryset = ProductModel.objects.all()
  serializer_class = ProductSerializer
#  permission_classes = [IsAuthenticated, IsAdmin]
  parser_classes = [MultiPartParser, FormParser]

  # Parametro para subir desde SWAGER la imagen del producto (formuDATA) 
  name_param = openapi.Parameter(
    'name',
    openapi.IN_FORM,
    type=openapi.TYPE_STRING,
    required=False,
    description='Nombre del producto'
  )
  image_param = openapi.Parameter(
    'image',
    openapi.IN_FORM,
    type=openapi.TYPE_FILE,
    required=False,
    description='Imagen del producto'
  )

  @swagger_auto_schema(
      tags=[ PRODUCT_TAG ],
      manual_parameters=[ image_param ],
      consumes=['multipart/form-data']
    )
  def put(self, request, *args, **kwargs):
    """ Actualiza un producto: metodo put """
    try:
      response = super().put(request, *args, **kwargs)
      return Response({
        'message': 'Producto actualizado exitosamente',
        'data': response.data
        }, status=status.HTTP_200_OK
      )
    except Http404:
      return Response({
        'message': 'Producto no encontrado',
        }, status=status.HTTP_404_NOT_FOUND)
  
  @swagger_auto_schema(
      tags=[ PRODUCT_TAG ],
      manual_parameters=[ name_param, image_param ],
      consumes=['multipart/form-data']
  )
  def patch(self, request, *args, **kwargs):
    """ Actualiza un producto: metodo patch """
    try:
      response = super().partial_update(request, *args, **kwargs)
      return Response({
        'message': 'Producto actualizado exitosamente',
        'data': response.data
        }, status=status.HTTP_200_OK)
    except Http404:
      return Response({
        'message': 'Producto no encontrado',
        }, status=status.HTTP_404_NOT_FOUND)
    
# Elimina un producto
class DeleteProductView(generics.DestroyAPIView):
  queryset = ProductModel.objects.all()
#  permission_classes = [IsAuthenticated, IsAdmin]

  @swagger_auto_schema(tags=[ PRODUCT_TAG ])
  def delete(self, request, *args, **kwargs):
    """ Elimina un producto: metodo delete """
    try:
      product = self.get_object()
      product.status = 'DELETED'
      product.save()
      return Response({
        'message': 'Producto eliminado exitosamente',
        }, status=status.HTTP_200_OK)
    except Http404:
      return Response({
        'message': 'Producto no encontrado',
        }, status=status.HTTP_404_NOT_FOUND) 

