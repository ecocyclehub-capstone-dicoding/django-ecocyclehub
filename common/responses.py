def format_error_response(message, errors, code):
    return {
        "success": False,
        "message": message,
        "code": str(code),
        "errors": errors
    }

def format_success_response(message, data, code):
    return {
        "success": True,
        "message": message,
        "code": str(code),
        "data": data
    }
