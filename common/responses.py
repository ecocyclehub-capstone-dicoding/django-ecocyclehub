def format_error_response(message, errors, code):
    return {
        "success": False,
        "message": message,
        "code": str(code),
        "errors": errors
    }