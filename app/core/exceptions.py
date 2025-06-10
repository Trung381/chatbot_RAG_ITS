class CustomException(Exception):
    def __init__(self, detail: str, status_code: int = 400, error_code: str = "GENERAL_ERROR"):
        self.detail = detail
        self.status_code = status_code
        self.error_code = error_code

class AuthenticationError(CustomException):
    def __init__(self, detail: str = "Authentication failed"):
        super().__init__(detail, 401, "AUTHENTICATION_ERROR")

class AuthorizationError(CustomException):
    def __init__(self, detail: str = "Not enough permissions"):
        super().__init__(detail, 403, "AUTHORIZATION_ERROR")

class NotFoundError(CustomException):
    def __init__(self, detail: str = "Resource not found"):
        super().__init__(detail, 404, "NOT_FOUND")

class ValidationError(CustomException):
    def __init__(self, detail: str = "Validation failed"):
        super().__init__(detail, 422, "VALIDATION_ERROR")
