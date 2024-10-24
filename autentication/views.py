from rest_framework import generics, status
from autentication.serializers import RoleModel, UserModel
from .serializers import RoleSerializer, UserSerializer, LoginSerializer
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema        # schema para el swagger
from rest_framework_simplejwt.views import (
  TokenObtainPairView,
)
from rest_framework.serializers import ValidationError
from .permissions import (
  IsAuthenticated,
  IsAdmin,
  IsSeller,
  IsSellerOrAdmin
)

# Crea un rol
class CreateRoleView(generics.CreateAPIView):
  queryset = RoleModel.objects.all()
  serializer_class = RoleSerializer

  """ Crea un nuevo rol """
  @swagger_auto_schema(tags=['Roles'])
  def post(self, request):
    response = super().post(request)

    return Response({
      'message': 'Role creado exitosamente',
      'data': response.data
    }, status=status.HTTP_201_CREATED
  )

# Lista todos los roles
class ListRoleView(generics.ListAPIView):
  queryset = RoleModel.objects.all()
  serializer_class = RoleSerializer

  """ Lista todos los roles """
  @swagger_auto_schema(tags=['Roles'])
  def get(self, request):
    response = super().get(request)

    return Response({
      'message': 'Roles listados exitosamente',
      'data': response.data
    }, status=status.HTTP_200_OK
  )

# crea un nuevo usuario
class CreateUserView(generics.CreateAPIView):
# queryset = UserModel.objects.all()
  serializer_class = UserSerializer

  @swagger_auto_schema(tags=['Usuarios'])
  def post(self, request):
    """ Crea un nuevo usuario """
    response = super().post(request)
    return Response({
      'message': 'Usuario creado exitosamente',
      'data': response.data
      }, status=status.HTTP_201_CREATED
    )
  
# Actualiza un usuario
class UpdateUserView(generics.UpdateAPIView):
  queryset = UserModel.objects.all()
  serializer_class = UserSerializer

  @swagger_auto_schema(tags=['Usuarios']) 
  def put(self, request, *args, **kwargs):
    response = super().put(request)

    return Response({
      'message': 'Usuario actualizado exitosamente',
      'data': response.data
      }, status=status.HTTP_200_OK
    )

  # Actualiza parcialmente un usuario
  @swagger_auto_schema(tags=['Usuarios'])
  def patch(self, request, *args, **kwargs):
    """ Actualiza parcialmente un usuario (metodo patch) """
    response = super().partial_update(request, *args, **kwargs)

    return Response({
      'message': 'Usuario actualizado exitosamente',
      'data': response.data
      }, status=status.HTTP_200_OK
    )

# Lista todos los usuarios
class ListUserView(generics.ListAPIView):
  queryset = UserModel.objects.all()
  serializer_class = UserSerializer
  permission_classes = [IsAuthenticated, IsAdmin]

  @swagger_auto_schema(tags=['Usuarios'])
  def get(self, request, *args, **kwargs):
    """ Lista todos los usuarios metodo get """
    response = super().get(request, *args, **kwargs)

    return Response({
      'message': 'Usuarios listados exitosamente',
      'data': response.data
      }, status=status.HTTP_200_OK
    )


class LoginView(TokenObtainPairView):
  serializer_class = LoginSerializer

  def post(self, request, *args, **kwargs):
    """ Recibe un token de autenticacion """
    try:
      return super().post(request, *args, **kwargs)
    except ValidationError as e:
      return Response({
        'message': 'Error al iniciar sesion',
      }, status=status.HTTP_401_UNAUTHORIZED
    )
    


