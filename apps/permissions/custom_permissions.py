from rest_framework.permissions import BasePermission
from .services import has_permission


class HasPermission(BasePermission):
    def __init__(self, permission_key):
        self.permission_key = permission_key

    def has_permission(self, request, view):
        return has_permission(request.user, self.permission_key)

class CanAddCategory(HasPermission):
    def __init__(self):
        super().__init__("add_categories")


class CanViewCategory(HasPermission):
    def __init__(self):
        super().__init__("view_categories")


class CanEditCategory(HasPermission):
    def __init__(self):
        super().__init__("edit_categories")


class CanDeleteCategory(HasPermission):
    def __init__(self):
        super().__init__("delete_categories")
