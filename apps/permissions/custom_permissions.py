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

class CanCreateTransaction(HasPermission):
    def __init__(self):
        super().__init__("create_transaction")

class CanViewTransaction(HasPermission):
    def __init__(self):
        super().__init__("view_transaction")

class CanVerifyTransaction(HasPermission):
    def __init__(self):
        super().__init__("verify_transaction")

class CanViewCustomerDashboard(HasPermission):
    def __init__(self):
        super().__init__("view_customer_dashboard")

class CanViewOfficerDashboard(HasPermission):
    def __init__(self):
        super().__init__("view_officer_dashboard")

class CanViewAdminDashboard(HasPermission):
    def __init__(self):
        super().__init__("view_admin_dashboard")

class CanAddLevel(HasPermission):
    def __init__(self):
        super().__init__("add_level")

class CanViewLevel(HasPermission):
    def __init__(self):
        super().__init__("view_level")

class CanEditLevel(HasPermission):
    def __init__(self):
        super().__init__("edit_level")

class CanDeleteLevel(HasPermission):
    def __init__(self):
        super().__init__("delete_level")
