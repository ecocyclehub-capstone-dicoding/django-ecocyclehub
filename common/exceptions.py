def handle_serializer_error(errors):
    is_required_error = any(
        "required" in str(err).lower()
        for field_errors in errors.values()
        for err in field_errors
    )

    is_duplicate = any(
        "already registered" in str(err).lower()
        for field_errors in errors.values()
        for err in field_errors
    )

    if is_duplicate:
        return {
            "response": {
                "success": False,
                "message": "Category already registered",
                "code": "409"
            },
            "status": 409
        }

    if is_required_error:
        return {
            "response": {
                "success": False,
                "message": "Some required fields are missing",
                "code": "422",
                "errors": errors
            },
            "status": 422
        }

    return {
        "response": {
            "success": False,
            "message": "Validation error",
            "code": "400",
            "errors": errors
        },
        "status": 400
    }
