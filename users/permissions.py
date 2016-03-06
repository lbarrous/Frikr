from rest_framework.permissions import BasePermission
#from users.api import UserDetailAPI



class UserPermission(BasePermission):

    def has_permission(self, request, view):
        """
        Define si el usuario autenticado en request.user tiene permiso para realizar la accion
        (GET, POST, PUT, DELETE)
        :return:
        """
        #from users.api import UserDetailAPI
        from users.api import UserViewSet
        # Si se quiere crear un usuario puede cualquiera
        if view.action == 'create':
            return True
        # Si no es POST, el superuser siempre puede
        elif request.user.is_superuser:
            return True
        # Si es un get a la vista de detalle, toma la decision has_boject_permissions
        elif view.action in ['retrieve', 'update', 'destroy']:
            return True
        else:
            # Get a lista de objetos
            return False

    def has_object_permission(self, request, view, obj):
        """
        Si el usuario autenticado en request.user tiene permiso para realizar la accion
        (GET, POST, PUT, DELETE) sobre el objeto obj
        """
        return request.user.is_superuser or request.user == obj