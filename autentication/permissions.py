from rest_framework.permissions import BasePermission
from rest_framework.exceptions import AuthenticationFailed


def is_authenticated(request):
  if not request.user.is_authenticated:
    raise AuthenticationFailed(detail={
        'message':'Credenciales incorrectas'
    }, code=401)

def is_role(request, role, message):
  if not request.user.role.name == role:
    raise AuthenticationFailed(detail={
        'message': f'No tienes permisos de {message}'
    }, code=403)


# Verifica si el usuario esta autenticado
class IsAuthenticated(BasePermission):
  def has_permission(self, request, view):
    is_authenticated(request)
    return True
  
# Verifica si el usuario es un administrador
class IsAdmin(BasePermission):
  def has_permission(self, request, view):
    is_authenticated(request)
    is_role(request, 'ADMIN', 'administrador')
    return True
  
# Verifica si el usuario es un vendedor
class IsSeller(BasePermission):
  def has_permission(self, request, view):
    is_authenticated(request)
    is_role(request, 'SELLER', 'vendedor')
    return True
  
# Verifica si el usuario es un vendedor o administrador
class IsSellerOrAdmin(BasePermission):
  def has_permission(self, request, view):
    is_authenticated(request)

    role = request.user.role.name
    if role == 'ADMIN' or role == 'SELLER':
      return True
    else:
      raise AuthenticationFailed(detail={
          'message': 'No tienes permisos de usuario'
        }, code=403)