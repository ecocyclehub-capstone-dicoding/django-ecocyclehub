def has_permission(user, permission_key):
    if not user or not user.is_authenticated:
        return False

    if not user.role:
        return False

    return user.role.permissions.filter(key=permission_key).exists()
